from django.db import models, transaction
import datetime
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate
from django.db.models.query import QuerySet
# Create your models here.


class PermException(Exception):
    pass


def get_field_changeable(obj):
    return [
        name for name in obj.__dict__.keys()
        if not (name.startswith('_') or name.endswith('id'))
        ]


@transaction.atomic
def change_model(obj, dic):
    field_changeable = get_field_changeable(obj)
    for key, value in dic.iteritems():
        if key not in field_changeable:
            raise PermException('field '+key+' is not changeable')
        obj.__dict__[key] = value
    obj.save()


class Book(models.Model):

    """the Book Model
    saved all Book related information.

    duartion : the duartion of the book
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
    rate = models.FloatField(default=0.0)
    rate_num = models.IntegerField(default=0.0)

    @staticmethod
    def _search_part(string):
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
        re = Book.objects.none()
        for ss in s:
            re = re | Book._search_part(ss)
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

    def get_comment(self):
        """get all comment about the book"""
        return self.comment_set.all()

    def __unicode__(self):  # only for debug
        return self.name_cn+" "+self.author+": "+str(self.duartion)+" " + \
            str(self.rate)


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
    species_admin = (
        (0, 'user'),
        (1, 'book manager'),
        (2, 'user manager'),
        )

    admin_type = models.IntegerField(choices=species_admin, default=0)

    def get_admin_type(self):
        return self.get_admin_type_display()

    @transaction.atomic
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

    @transaction.atomic
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

    def has_borrowing_num(self):
        """return the number of book which you have borrowed."""
        return Borrowing.objects.filter(
            myuser=self, status__in=[0, 1, 2], is_active=True
            ).count()

    def has_queue_num(self):
        """return the number of book wich you have queued."""
        return Borrowing.objects.filter(
            myuser=self, status=4, is_active=True
            ).count()

    def get_all_borrowing(self):
        bo =  Borrowing.objects.filter(
            myuser=self, status__in=[0, 1, 2], is_active=True
            )
        re = []
        for borr in bo:
            re.append(borr.book_copy)
        return re

    def get_all_queue(self):
        bo =  Borrowing.objects.filter(
            myuser=self, status=4, is_active=True
            )
        re = []
        for borr in bo:
            re.append(borr.book_copy)
        return re

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
        if (book_copy.get_status()['text'] != 'on shelf'):
            raise PermException("the book is not on shelf")
        elif (myuser.has_borrowing_num >= myuser.has_perm('borrowing_num')):
            raise PermException("you can't borrow so many book~")
        else:
            Borrowing.objects.create(
                status=0,
                book_copy=book_copy,
                myuser=myuser,
                )

    @staticmethod
    def reborrow(myuser, book_copy):
        """User myuser reborrow the book again."""
        if (not Borrowing.objects.filter(
                myuser=myuser, book_copy=book_copy, is_active=True,
                status__in=[0, 1, 2]
                ).exists()):
            raise PermException("you don't borrow this book!")
        elif (book_copy.get_status()['queue'] > 0):
            raise PermException("there is someone queuing, you can't reborrow")
        elif (Borrowing.objects.get(
                is_active=True, myuser=myuser, book_copy=book_copy
                ).status == 2):
            raise PermException("you have reborrowed once!")
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
    @transaction.atomic
    def return_book(book_copy):
        """User myuser return the book"""
        if (not Borrowing.objects.filter(
                book_copy=book_copy, is_active=True,
                status__in=[0, 1, 2]
                ).exists()):
            raise PermException("noone borrows this book!")
        b = Borrowing.objects.get(
            is_active=True, status__in=[0, 1, 2], book_copy=book_copy
            )
        myuser = b.myuser
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
        if (not Borrowing.objects.filter(
                is_active=True, status=3, book_copy=book_copy
                ).exists()):
            raise PermException("the book is not arranging")
        elif (not Borrowing.objects.filter(
                is_active=True, status=4, book_copy=book_copy
                ).exists()):
            raise PermException("no one queue")
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
        if (not Borrowing.objects.filter(
                is_active=True, status=3, book_copy=book_copy
                ).exists()):
            raise PermException("the book is not arranging")
        b = Borrowing.objects.get(
            is_active=True, status=3, book_copy=book_copy
            )
        b.is_active = False
        b.save()
        Borrowing.objects.filter(
                is_active=True, status=4, book_copy=book_copy
                ).update(is_active=False)

    @staticmethod
    def queue(myuser, book_copy):
        if (Borrowing.objects.filter(
                myuser=myuser, book_copy=book_copy, is_active=True, status=0
                ).exists()):
            raise PermException("you have been borrowing this book!")
        elif (Borrowing.objects.filter(
                myuser=myuser, book_copy=book_copy, is_active=True, status=4
                ).exists()):
            raise PermException("you have been queuing this book!")
        elif (myuser.get_perm("queue_book_num") <= myuser.has_queue_num()):
            raise PermException("you can't queue so many books.")
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
    def disappear(book_copy):
        """the book which myuser borrowed has disappeared"""
        if (not Borrowing.objects.filter(
                book_copy=book_copy, is_active=True,
                status__in=[0, 1, 2]
                ).exists()):
            raise PermException("noone borrows this book!")
        b = Borrowing.objects.get(
            is_active=True, status__in=[0, 1, 2], book_copy=book_copy
            )
        myuser = b.myuser
        bs = Borrowing.objects.filter(
            is_active=True, book_copy=book_copy
            )
        bs.update(is_active=False)
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
        """get all info with species sp."""
        if sp is None:
            return Info.objects.all()
        str2id = {sp_name: sp_id for sp_id, sp_name in Info.species_choice}
        return Info.objects.filter(species=str2id[sp])

    def local_time(self):
        """get local time of publish the info"""
        return timezone.localtime(self.date)

    def __unicode__(self):  # only for debug
        return self.title+" "+str(self.date)


class Comment(models.Model):
    """the comment of book"""

    species_rate = (
        (1, 'perfect'),
        (2, 'good'),
        (3, 'normal'),
        (4, 'bad'),
        (5, 'terrible'),
    )
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=10000)
    datetime = models.DateTimeField(auto_now=True)
    rate = models.IntegerField(choices=species_rate, default=3)
    spoiler = models.BooleanField(default=False)
    myuser = models.ForeignKey(MyUser)
    book = models.ForeignKey(Book)

    def _update(self):
        """update the rate of the book after comment"""
        self.book.rate = (self.book.rate*self.book.rate_num+self.rate) / \
            (self.book.rate_num+1)
        self.book.rate_num = self.book.rate_num+1
        self.book.save()

    @staticmethod
    def add(myuser, book, title, content, rate=3, spoiler=False):
        """add a new comment"""
        c = Comment.objects.create(
            myuser=myuser,
            book=book,
            title=title,
            content=content,
            rate=rate,
            spoiler=spoiler,
            )
        c._update()

    @transaction.atomic
    def remove(self):
        if self.book.rate_num == 1:
            self.book.rate = 0.0
        else:
            self.book.rate = (self.book.rate*self.book.rate_num-self.rate) / \
                (self.book.rate_num-1)
        self.book.rate_num = self.book.rate_num-1
        self.book.save()
        self.delete()

    def __unicode__(self):  # only for debug
        return self.myuser.name+" "+self.book.simple_name()+" " + \
            self.title+" : "+self.content+" "+str(self.rate)


class Rank(models.Model):
    """save range every month"""

    RANK_NUM = 10
    version = models.IntegerField()
    book = models.ForeignKey(Book)
    value = models.FloatField()
    species_sort_method = (
        (0, 'borrowing time'),
        (1, 'comment number'),
        (2, 'rate')
    )
    sort_method = models.IntegerField(choices=species_sort_method)
    rank = models.IntegerField()

    @staticmethod
    def get_maxversion():
        agg = Rank.objects.all().aggregate(models.Max('version'))
        n = agg['version__max']
        if agg['version__max'] is None:
            n = 0
        return n

    @staticmethod
    def _cal_value(books, species):
        re = []
        for book in books:
            if species == 0:
                n = 0
                for bookcopy in book.bookcopy_set.all():
                    n += Borrowing.objects.filter(
                        book_copy=bookcopy, status__in=[0, 1, 2]
                        ).count()
                re.append(n)
            elif species == 1:
                re.append(book.rate_num)
            elif species == 2:
                re.append(book.rate)
        return re

    @staticmethod
    @transaction.atomic
    def _top10(species, version):
        """get top 10 by species_sort_method"""
        books = list(Book.objects.all())
        values = Rank._cal_value(books, species)
        l = zip(books, values)
        l.sort(key=lambda a: a[1], reverse=True)
        l = l[:Rank.RANK_NUM]
        for index, i in enumerate(l):
            Rank.objects.create(
                version=version,
                book=i[0],
                value=i[1],
                sort_method=species,
                rank=index,
                )

    @staticmethod
    def update():
        """update the rank every week!"""
        version = Rank.get_maxversion()+1
        for i in range(len(Rank.species_sort_method)):
            Rank._top10(i, version)

    @staticmethod
    def get_top(species=2, v=0):
        if v == 0:
            v = Rank.get_maxversion()
        return Rank.objects.filter(
            version=v, sort_method=species
            ).order_by('rank')

    def __unicode__(self):
        return self.book.simple_name()+" "+str(self.value)+" " + \
            str(self.sort_method)+" "+str(self.rank)
