from django.db import models, transaction
import datetime
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate
from django.db.models.query import QuerySet
# Create your models here.


class Book(models.Model):

    """the Book Model
    saved all Book related information.
    """

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
        """search for string in name_cn, name_origin or author"""
        re1 = Book.objects.filter(name_cn__contains=string)
        re2 = Book.objects.filter(name_origin__contains=string)
        re3 = Book.objects.filter(author__contains=string)
        return re1 | re2 | re3

    @staticmethod
    def search(string):
        """
        make the word split with whitespace and get their search result union.
        """
        s = string.split()
        re = Book.objects.get_empty_query_set()
        for ss in s:
            re = re | Book.search_part(ss)
        return re

    def simple_name(self):
        """return a simple name"""
        if self.name_cn == "":
            return self.name_origin
        return self.name_cn

    def simple_version(self):
        """return a simple version"""
        return 'ver %d, %d (Origin: ver %d, %d)' % (
            self.revision, self.pub_year,
            self.revision_origin, self.pub_year_origin,
            )

    def __unicode__(self):  # only for debug
        return self.name_cn+" "+self.author+": "+str(self.duartion)


class BookCopy(models.Model):

    """the BookCopy model
    saved information of BookCopy. as a foreign key of book.
    """

    book = models.ForeignKey(Book)
    location = models.CharField(max_length=100)

    def get_status(self):
        """
        Do get the book status, return a dict.
        """
        re = {}
        all_borrowing = self.borrowing_set.filter(is_active=True)
        if all_borrowing.filter(status__in=[0, 1, 2]).exists():
            borr = all_borrowing.get(status__in=[0, 1, 2])
            k = borr.myuser.get_perm('borrowing_coefficient') * \
                borr.book_copy.book.duartion
            re = {'text': 'borrowing'}
            re['expire'] = borr.datetime.date() + datetime.timedelta(days=k)
            re['reborrow_count'] = borr.status
            re['queue'] = all_borrowing.filter(status=4).count()
        elif all_borrowing.filter(status=3).exists():
            re = {'text': 'arranging'}
        elif all_borrowing.filter(status=5).exists():
            re = {'text': 'disappear'}
        else:
            re = {'text': 'on shelf'}
        return re

    def __unicode__(self):  # only for debug
        return str(self.id) + ": " + self.book.simple_name()


class MyUser(models.Model):

    """the myuser model.
    extend Django.User model, as a one-to-one relationship with Django.User.
    add group and permission.
    """

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

    def _permission_num_generate(*args):
        """generate permission number list"""
        permission_num_list = [
            'borrowing_num', 'borrowing_coefficient', 'queue_book_num'
            ]  # TODO: Remove this dumplicated definition!
        return dict(zip(permission_num_list, args))

    permission_num = {
        'NormalUser': _permission_num_generate(10, 1, 1),
        'AdvancedUser': _permission_num_generate(20, 2, 3),
        'Blacklist': _permission_num_generate(0, 0, 0),
        'Admin': _permission_num_generate(0, 0, 0),
        }

    @transaction.commit_on_success
    def register(self, username, password, email, name, group='NormalUser'):
        """
        user register,
        Usage():
            >>> myuser = MyUser()
            >>> myuser.register(username, password, email, name, group)
        """
        u = User.objects.create_user(username, email, password)
        self.user = u
        self.name = name
        if group in self.group_list:
            self.set_group(group)
        else:
            raise TypeError()
        self.save()

    def set_group(self, group):
        """set user group"""
        g = Group.objects.get(name=group)
        self.user.groups = [g]
        self.user.save()

    def get_group_name(self):
        """get my group name"""
        return self.user.groups.all()[0].name

    def get_group(self):
        """get my group queryset"""
        return self.user.groups.all()

    @transaction.commit_on_success
    def erase(self):
        """delete user in both myuser and Django.User"""
        self.user.delete()
        self.delete()

    def has_perm(self, perm):
        """return whether has the permission"""
        return self.user.has_perm('rt.'+perm)

    def get_perm(self, perm):
        """return the permission numbe"""
        return (self.permission_num[self.get_group_name()])[perm]

    def __unicode__(self):
        return self.name


class Borrowing(models.Model):

    """the borrowing model
    saves the user borrowing information
    """

    status_choice = (
        (0, 'borrowing'),
        (1, 'reborrowing 1'),
        (2, 'reborrowing 2'),
        (3, 'arranging'),
        (4, 'queue'),
        (5, 'disappear'),
        )
    status = models.IntegerField(choices=status_choice)
    datetime = models.DateTimeField(auto_now=True)
    book_copy = models.ForeignKey(BookCopy)
    myuser = models.ForeignKey(MyUser)
    is_active = models.BooleanField(default=True)

    @staticmethod
    def borrow(myuser, book_copy):
        """User myuser borrow a book_copy."""
        Borrowing.objects.create(
            status=0,
            book_copy=book_copy,
            myuser=myuser,
            )

    @staticmethod
    def reborrow(myuser, book_copy):
        """User muuser reborrow the book again."""
        b = Borrowing.objects.get(
            is_active=True, myuser=myuser, book_copy=book_copy
            )
        b.is_active = False
        b.save()
        Borrowing.objects.create(
            status=b.status+1,
            book_copy=book_copy,
            myuser=myuser,
            )

    @staticmethod
    def return_book(myuser, book_copy):
        """User myuser return the book"""
        b = Borrowing.objects.get(
            is_active=True, myuser=myuser, book_copy=book_copy
            )
        b.is_active = False
        b.save()
        Borrowing.objects.create(
            status=3,
            book_copy=book_copy,
            myuser=myuser,
            )

    @staticmethod
    def queue_next(book_copy):
        """the admin gives the returned book to the one who queue first."""
        b = Borrowing.objects.get(
            is_active=True, status=3, book_copy=book_copy
            )
        b.is_active = False
        b.save()
        u = Borrowing.objects.filter(
            is_active=True, status=4, book_copy=book_copy
            ).order_by('datetime')[0]
        u.is_active = False
        u.save()
        Borrowing.objects.create(
            status=0,
            book_copy=book_copy,
            myuser=u.myuser,
            )

    @staticmethod
    def readify(book_copy):
        """the admin moves the returned book to shelf."""
        b = Borrowing.objects.get(
            is_active=True, status=3, book_copy=book_copy
            )
        b.is_active = False
        b.save()
        for u in Borrowing.objects.filter(
                is_active=True, status=4, book_copy=book_copy
                ):
            u.is_active = False
            u.save()

    @staticmethod
    def queue(myuser, book_copy):
        """queue a book."""
        if (
            Borrowing.objects.filter(
                is_active=True, status__in=[0, 1, 2], book_copy=book_copy
                ).exists()):
            Borrowing.objects.create(
                status=4,
                book_copy=book_copy,
                myuser=myuser,
                )

    @staticmethod
    def disappear(myuser, book_copy):
        """the book which myuser borrowed has disappeared"""
        bs = Borrowing.objects.filter(
            is_active=True, book_copy=book_copy
            )
        for b in bs:
            b.is_active = False
            b.save()
        Borrowing.objects.create(
            status=5,
            book_copy=book_copy,
            myuser=myuser,
            )

    def __unicode__(self):  # only for debug
        return self.myuser.name + " " + str(self.book_copy.id) + ":" + \
            self.book_copy.book.simple_name() + \
            " " + self.get_status_display()


class Info(models.Model):

    """the model info
    saved the info in home page.
    """

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
        """get all info with speices sp."""
        if sp is None:
            return Info.objects.all()
        str2id = {sp_name: sp_id for sp_id, sp_name in Info.species_choice}
        return Info.objects.filter(species=str2id[sp])

    def local_time(self):
        """get local time of publish the info"""
        return timezone.localtime(self.date)

    def __unicode__(self):  # only for debug
        return self.title+" "+str(self.date)
