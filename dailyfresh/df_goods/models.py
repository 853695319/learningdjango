from django.db import models
from ckeditor.fields import RichTextField


class TypeInfo(models.Model):
    """商品分类"""
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)


class GoodsInfo(models.Model):
    """商品信息"""
    gtitle = models.CharField(max_length=20)

    # upload to MEDIA_ROOT/da_goods/
    gpic = models.ImageField(upload_to='df_goods')
    gprice = models.DecimalField(max_digits=5, decimal_places=2)
    gunit = models.CharField(max_length=20)
    gclick = models.IntegerField()
    gjianjie = models.CharField(max_length=200)
    gkucun = models.IntegerField()

    # 富文本编辑器
    gcontent = RichTextField()
    isDelete = models.BooleanField(default=False)
    gtype = models.ForeignKey('TypeInfo')
    # gadv = models.BooleanField(default=False)
