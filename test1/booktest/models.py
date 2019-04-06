from django.db import models

# Create your models here.


class BookInfo(models.Model):
    """图书结构"""
    # 定义类属性，是为了映射数据库中的相应字段，通过类创建的实例对象是不能操作类属性的
    # 类属性生成表结构的依据
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField()

    def __str__(self):
        return self.btitle
        # return self.btitle.encode('utf-8') 可能跟版本有关，视频里需要设置编码，而为这个版本要求string not byte


class HeroInfo(models.Model):
    """英雄结构"""
    hname = models.CharField(max_length=10)
    hgender = models.BooleanField()
    hcontent = models.CharField(max_length=1000)
    # 引入外键
    hbook = models.ForeignKey(BookInfo)

    def __str__(self):
        return self.hname

    def gender(self):
        """布尔值显示性别"""
        if self.hgender:
            return "男"
        else:
            return "女"

    gender.short_description = '性别'

"""
In [1]: class Person(object):
   ...:     name = 'Person'
   ...:     def __str__(self):
   ...:         return self.name
   ...:     

In [2]: p = Person()

In [3]: p.name = 'p'

In [4]: print(p)
p

In [5]: Person.name
Out[5]: 'Person'

同理，下面这个也没错，类属性并没有被修改，是用来映射数据库字段的
from booktest.models import *
b = BookInfo()
b.btitle = 'abc'
为什么一定要用相同的属性名呢？
b.save()
调用save方法的时候类似 SQL INSERT 方法，将数据插入对应的字段中,所以属性名一定要一样
不用担心修改到类属性
"""