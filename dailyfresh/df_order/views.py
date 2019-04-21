from django.shortcuts import render
from .models import *
from .user_decorator import login_wrapper
from django.db import transaction


@login_wrapper
def order(request):
    """渲染订单页面"""
    cart_ids = request.GET.getlist('cartid')

    context = {
        'title': '提交订单',
        'user_page': 1,

    }
    return render(request, 'df_order/place_order.html', context)


@transaction.atomic()
@login_wrapper
def order_handle(request):
    """
    事物： 一旦操作失败则全部回退
    1 创建订单对象
    2 判断商品的库存
    3 创建详单对象
    4 修改商品库存
    5 删除购物车
    """

    # 存档，用于将来回退
    tran_id = transaction.savepoint()

    # 接收购物车ID
    cart_ids = request.POST.get('cart_ids')
    return

