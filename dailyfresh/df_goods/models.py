from django.db import models
from ckeditor.fields import RichTextField


class TypeInfo(models.Model):
    """商品分类"""
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle


class GoodsInfo(models.Model):
    """商品信息"""
    gtitle = models.CharField(max_length=20)  # 名字
    gpic = models.ImageField(upload_to='df_goods')  # 图片 upload to MEDIA_ROOT/da_goods/
    gprice = models.DecimalField(max_digits=5, decimal_places=2)  # 价格
    gunit = models.CharField(max_length=20)  # 单位
    gclick = models.IntegerField()  # 点击量
    gjianjie = models.CharField(max_length=200)  # 简介
    gkucun = models.IntegerField()  # 库存
    gcontent = RichTextField()  # 富文本编辑器
    isDelete = models.BooleanField(default=False)  # 逻辑删除
    gtype = models.ForeignKey('TypeInfo')  # 分类
    # gadv = models.BooleanField(default=False)

    def __str__(self):
        return self.gtitle


"""
快速制造测试数据
>>> python manage.py shell
>>> for i in range(20):
...     good = GoodsInfo()
...     good.gtitle = '速冻食品%d' % i
...     good.gpic = 'df_goods/goods009.jpg'
...     good.gprice = 10.51 + i + i * 0.1
...     good.gunit = '500g'
...     good.gclick = 30 + i
...     good.gjianjie = '简介：速冻食品-%d' % i
...     good.gkucun = i*25
...     good.gcontent = good.gtitle * 2
...     good.gtype_id = 6
...     good.save()

for i in range(20):
    good = GoodsInfo()
    good.gtitle = '速冻食品%d' % i
    good.gpic = 'df_goods/goods009.jpg'
    good.gprice = 10.51 + i + i * 0.1
    good.gunit = '500g'
    good.gclick = 30 + i
    good.gjianjie = '简介：速冻食品-%d' % i
    good.gkucun = i*25
    good.gcontent = good.gtitle * 2
    good.gtype_id = 6
    good.save()
"""