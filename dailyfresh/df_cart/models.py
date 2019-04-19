from django.db import models


class CartInfo(models.Model):
    # 引用其他应用的模型
    user = models.ForeignKey('df_user.UserInfo')
    goods = models.ForeignKey('df_goods.GoodsInfo')
    count = models.IntegerField()

