from django.db import models

# Create your models here.


class BookInfoManager(models.Manager):
    """自定义Manager，模型类的管理器"""
    def get_queryset(self):
        """重写管理器Manager的get_querset方法，返回未逻辑删除的对象"""
        return super(BookInfoManager, self).get_queryset().filter(isDelete=False)

    def create(self, btitle, bpub_date, bread=0, bcomment=0, isDelete=False):
        """创建对象"""
        b = BookInfo()
        b.btitle = btitle
        b.bpub_date = bpub_date
        b.bread = bread
        b.bcomment = bcomment
        b.isDelete = isDelete
        return b


class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField(db_column='pub_date')  # 设置admin字段名为pub_date
    # 阅读量，顺便测试default有没有用
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(null=False)  # 评论量不能为空
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.btitle

    # 定义元信息
    class Meta:
        db_table = 'bookinfo'  # 定义数据表名称,默认表名为 booktest_bookinfo

    book1 = models.Manager()  # 指定管理器,默认管理器object就不给你了
    book2 = BookInfoManager()  # 自定义管理器

    # 希望更加快捷的生成实例对象
    # Warning:不能用 __init__()方法，原因是父类models.Model已经用了__init__方法了

    # 类方法创建对象
    @classmethod
    def create(cls, btitle, bpub_date, bread=0, bcomment=0, isDelete=False):
        b = BookInfo()
        b.btitle = btitle
        b.bpub_date = bpub_date
        b.bread = bread
        b.bcomment = bcomment
        b.isDelete = isDelete
        return b


class HeroInfo(models.Model):
    hname = models.CharField(max_length=10)
    hgender = models.BooleanField(default=True)
    hcontent = models.CharField(max_length=1000)
    idDelete = models.BooleanField(default=False)
    book = models.ForeignKey(BookInfo)

    def __str__(self):
        return self.hname

    def gender(self):
        if self.hgender:
            return '男'
        else:
            return '女'
    gender.short_description = '性别'


