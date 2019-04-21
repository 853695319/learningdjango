from django.db import models


class OrderInfo(models.Model):
    """订单主表"""
    oid = models.CharField(max_length=20, primary_key=True)  # 订单编号
    user = models.ForeignKey('df_user.UserInfo')  # 用户
    # 每次保存对象时，自动设置该字段为当前时间。 用于"最后一次修改"的时间戳
    # 保存到数据库的时UTC时间
    # 渲染到模板时会根据TIME_ZONE匹配本地事件
    odate = models.DateTimeField(auto_now=True)
    oIsPay = models.BooleanField(default=False)
    # 用的情况不较多，经常聚合对服务器压力大
    ototal = models.DecimalField(max_digits=6, decimal_places=2)
    oaddr = models.CharField(max_length=150)  # 跟用户模型一致

    # 目前无法实现：真实支付，物流信息


class OrderDetailInfo(models.Model):
    """订单详情"""
    goods = models.ForeignKey('df_goods.GoodsInfo')
    order = models.ForeignKey(OrderInfo)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    count = models.IntegerField()


