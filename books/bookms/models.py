from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.
class Publishers(models.Model):
    name = models.CharField("出版社", max_length=128)

    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField("分类", max_length=64)

    def __str__(self):
        return self.name


class Authors(models.Model):
    SEX_CHOICE = (
        (0, '男'),
        (1, '女'),
    )

    name = models.CharField("姓名", max_length=128)
    sex = models.IntegerField(choices=SEX_CHOICE)
    birthday = models.DateField("生日", null=True)
    date_death = models.DateField(null=True)
    nation = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Books(models.Model):
    name = models.CharField("书名", max_length=128)
    inc_date = models.DateField("入库日期", default=datetime.datetime.now)
    isbn = models.CharField("索书号", max_length=128, unique=True, primary_key=True)
    num_copies = models.IntegerField("副本", default=1)
    num_lend = models.IntegerField("借出数", default=0)
    publisher = models.ForeignKey(Publishers, on_delete=models.CASCADE)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    rate = models.FloatField(null=True)

    def __str__(self):
        return self.name

    def is_included_recently(self):
        return self.inc_date > datetime.datetime.now().date() - datetime.timedelta(days=14)


class Readers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reader_identity = models.IntegerField("读者证编号")
    reg_date = models.DateField(default=datetime.datetime.now)
    age = models.IntegerField(null=True)
    delay_times = models.IntegerField(default=0)
    forbid = models.BooleanField(default=False)
    forbid_date = models.DateField(null=True)
    latest_borrowed_category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

    def is_unforbid(self):
        return self.forbid_date < datetime.datetime.now().date() - datetime.timedelta(days=365)


class Borrows(models.Model):
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.datetime.now)
    repeat = models.IntegerField(default=0)

    def __str__(self):
        return self.book.name + ',' + self.reader.user.username

    def is_overdue(self):
        days = 60 * (self.repeat + 1)
        return self.date < datetime.datetime.now().date() - datetime.timedelta(days=days)

    def nearly_overdue(self):
        days = 60 * (self.repeat + 1)
        return self.date + datetime.timedelta(days=days) - datetime.datetime.now().date() < datetime.timedelta(days=5)


class Borrow_histry(models.Model):
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return self.reader.user.username+ ',' + self.book.name

class Ratings(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    rate = models.FloatField(null=True, default=None)
    comment = models.TextField(verbose_name="评论", null=True, default=None)

    def __str__(self):
        return [self.book.name, self.reader.user.username, self.rate]