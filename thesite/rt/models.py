from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate
from django.db.models.query import QuerySet
# Create your models here.


class Book(models.Model):
    duartion = models.SmallIntegerField(default=14)  # It can only be 0, 7, 14
    name_cn = models.CharField(max_length=200, default="")
    author = models.CharField(max_length=300)  # separate by ","
    press = models.CharField(max_length=200)
    pub_year = models.SmallIntegerField(default=1900)
    revision = models.SmallIntegerField(default=0)
    ISBN = models.CharField(max_length=50)
    name_origin = models.CharField(max_length=200, default="")
    translator = models.CharField(max_length=200, default="")
    pub_year_origin = models.SmallIntegerField(default=1900)
    revision_origin = models.SmallIntegerField(default=0)

    @staticmethod
    def search_part(string):
        re1 = Book.objects.filter(name_cn__contains=string)
        re2 = Book.objects.filter(name_origin__contains=string)
        re3 = Book.objects.filter(author__contains=string)
        return re1 | re2 | re3

    @staticmethod
    def search(string):
        s = string.split()
        re = Book.objects.get_empty_query_set()
        for ss in s:
            re = re | Book.search_part(ss)
        return re

    def simple_name(self):
        if self.name_cn == "":
            return self.name_origin
        return self.name_cn

    def simple_version(self):
        return 'ver %d, %d (Origin: ver %d, %d)' % (
            self.revision, self.pub_year,
            self.revision_origin, self.pub_year_origin,
            )

    def __unicode__(self):  # only for debug
        return self.name_cn+" "+self.author+": "+str(self.duartion)


class BookCopy(models.Model):
    status_choice = (
        (0, 'ready'),
        (1, 'unreturned'),
        (2, 'over time'),
        (3, 'arranging'),
        (4, 'off shelf')
    )
    status = models.IntegerField(choices=status_choice, default=0)
    book = models.ForeignKey(Book)
    reborrow_time = models.SmallIntegerField(default=0)
    location = models.CharField(max_length=100)

    def __unicode__(self):  # only for debug
        return str(self.id) + ": " + self.book.simple_name() + ": " + \
            self.get_status_display()


class MyUser(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=100)
    group_list = ['NormalUser', 'AdvancedUser', 'Blacklist', 'Admin']  # guest
    permission_list = ['can_search', 'can_comment', 'can_manage']
    """
    'can_manage' includes ('can_midify_book', 'can_change_perm',
    'can_generate_tempuser', 'can_manage_blacklist', 'can_delete_user')
    """
    permission_num_list = [
        'borrowing_num', 'borrowing_coefficient', 'queue_book_num'
        ]
    def _permission_num_generate(self, *args):
        return dict(zip(self.permission_num_list, args))

    def __init__(self):
        self.permission_num = {
            'NormalUser': self._permission_num_generate(10, 1, 1),
            'AdvancedUser': self._permission_num_generate(20, 2, 3),
            'Blacklist': self._permission_num_generate(0, 0, 0),
            'Admin': self._permission_num_generate(0, 0, 0),
            }

    def register(self, username, password, email, name, group='NormalUser'):
        '''
            >>> myuser = MyUser()
            >>> myuser.register(username, password, email, name, group)
        '''
        u = User(username=username, email=email, password=password)
        u.save()
        self.user = u
        self.name = name
        if group in self.group_list:
            self.set_group(group)
        else:
            raise TypeError()
        self.user.save()
        self.save()

    def set_group(self, group):
        g = Group.objects.get(name=group)
        self.user.groups = [g]
        self.user.save()

    def get_group_name(self):
        return self.user.groups.all()[0].name

    def get_group(self):
        return self.user.groups.all()

    def delete(self):
        self.user.delete()
        super(MyUser, self).delete()

    def has_perm(self, perm):
        return self.user.has_perm('rt.'+perm)

    def get_perm(self, perm):
        return (self.permission_num[self.get_group_name()])[perm]

    def __unicode__(self):
        return self.name


class Borrowing(models.Model):
    status_choice = (
        (0, 'borrowing'),
        (1, 'unreturned'),
        (2, 'over time'),
        (3, 'arranging'),
        (4, 'off shelf')
        )
    status = models.IntegerField(choices=status_choice)
    date_borrowing = models.DateField(auto_now=True)
    date_return = models.DateField()
    book_copy = models.ForeignKey(BookCopy)
    myuser = models.ForeignKey(MyUser)
    reborrow_time = models.SmallIntegerField(default=0)

    def date_expired(self):
        return date_borrowing+datetime.timedelta(days=book_copy.book.duartion)


class Info(models.Model):
    species_choice = (
        (0, 'news'),
        (1, 'guide'),
    )
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=10000)
    date = models.DateTimeField(auto_now=True)
    species = models.IntegerField(choices=species_choice, default=0)

    @staticmethod
    def get_all(sp=None):
        if sp is None:
            return Info.objects.all()
        str2id = {sp_name: sp_id for sp_id, sp_name in Info.species_choice}
        return Info.objects.filter(species=str2id[sp])

    def local_time(self):
        return timezone.localtime(self.date)

    def __unicode__(self):  # only for debug
        return self.title+" "+str(self.date)
