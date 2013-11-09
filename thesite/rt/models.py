from django.db import models
import datetime
from django.utils import timezone

# Create your models here.


class Book(models.Model):
    duartion = models.SmallIntegerField(default=0)  # It can only be 0, 7, 14
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

    def simple_name(self):
        if self.name_cn == "":
            return self.name_origin
        return self.name_cn

    def __unicode__(self):  # only for debbug
        return self.name_cn+" "+self.author+": "+str(self.duartion)


class BookCopy(models.Models):
    status_choice = (
        (0, 'ready'),
        (1, 'unreturned'),
        (2, 'over time')
        (3, 'arranging'),
        (4, 'off shelf')
    )
    status = models.IntegerField(choices=status_choice)
    book = models.ForeignKey(BookCopy)
    reborrow_time = models.SmallIntegerField(default=0)


class Borrowing(models.Model):
    status_choice = (
        (0, 'borrowing'),
        (1, 'unreturned'),
        (2, 'over time'),
        (3, 'arranging'),
        (4, 'off shelf')
        )
    status = models.IntegerField(choices=status_choice)
    date_borrowing = models.DateField(default=timezone.now().date())
    date_return = models.DateField()
    book_copy = models.ForeignKey(BookCopy)
    reborrow_time = models.SmallIntegerField(default=0)

    def date_expired(self):
        return date_borrowing + datetime.timedelta(days=book.duartion)
