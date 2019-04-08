from django.db import models


class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField(db_column='pub_date')
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(null=False)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.btitle

    class Meta:
        db_table = 'bookinfo'


class HeroInfo(models.Model):
    hname = models.CharField(max_length=10)
    hgender = models.BooleanField(default=True)
    hcontent = models.CharField(max_length=1000)
    idDelete = models.BooleanField(default=False)
    book = models.ForeignKey(BookInfo)

    def __str__(self):
        return self.hname