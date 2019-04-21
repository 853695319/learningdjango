from django.shortcuts import render, redirect
from .models import *
from .user_decorator import login_wrapper
from django.db import transaction
from df_cart.models import CartInfo
from df_user.models import UserInfo
from django.http import JsonResponse
import datetime, decimal


@login_wrapper
def order(request):
    """渲染提交订单页面"""
    # 取的提交的商品信息
    cart_ids = request.GET.getlist('cartid', '')
    if not len(cart_ids):
        # 如果什么商品信息都没有，跳转会主页
        return redirect('/')
    cart_set = CartInfo.objects.filter(id__in=cart_ids)
    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)

    context = {
        # 模板
        'title': '提交订单',
        'order_page': 1,
        # 返回参数
        'user': user,
        'cart_set': cart_set
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
    cart_ids = request.POST.getlist('cart_ids[]', '')

    # test post
    # print("{0}\n{1}".format('*'*10, cart_ids))
    # if cart_ids:
    #     data = {'code': 200}
    # else:
    #     date = {'code': 404}


    try:
        # 1 创建订单对象
        orderinfo = OrderInfo()
        now = datetime.datetime.now()
        uid = request.session.get('user_id')
        # 订单编号由日期+用户id构成
        # __format__或strftime,将datetime实例按格式生成字符串
        orderinfo.oid = '{}{}'.format(now.__format__('%Y%m%d%H%M%S'), uid)
        print("{0}\n{1}".format('*'*10, orderinfo.oid))
        orderinfo.user_id = uid
        # 高精度浮点数
        orderinfo.ototal = decimal.Decimal(request.POST.get('total'))
        # 我没有设在odate，我想看他会不会自己生成
        orderinfo.save()

        # 创建详单对象
        for cid in cart_ids:
            detailinfo = OrderDetailInfo()
            cart = CartInfo.objects.get(id=cid)
            detailinfo.goods = cart.goods
            detailinfo.order = orderinfo
            detailinfo.price = cart.goods.gprice
            detailinfo.count = cart.count

    except Exception as err:
        # 如果出现异常
        print("{0}\n{1}".format('*'*10, err))
        # tran_id.

    return JsonResponse(data)

