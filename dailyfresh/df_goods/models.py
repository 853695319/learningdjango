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
