from django.shortcuts import render, redirect, reverse
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
    #     data = {'url': reverse('user:order')}
    # else:
    #     date = {'url': 404}
    # return JsonResponse(data)

    try:
        # 1 创建订单对象
        orderinfo = OrderInfo()

        # 订单编号由日期+用户id构成
        # __format__或strftime,将datetime实例按格式生成字符串
        now = datetime.datetime.now()
        uid = request.session.get('user_id')
        orderinfo.oid = '{}{}'.format(now.__format__('%Y%m%d%H%M%S'), uid)
        print("{0}\n{1}".format('*'*10, orderinfo.oid))

        # 用户
        orderinfo.user_id = uid

        # 总计 高精度浮点数
        orderinfo.ototal = decimal.Decimal(request.POST.get('total'))

        # 收获地址
        orderinfo.oaddr = request.POST.get('uaddr')

        # odate在每次保存时会自动设置，且时区为UTC，慢8小时，不过不影响，反正这个时间在后台也不显示的
        # 时区转换 time.astimezone(pytz.timezone('Asia/Shanghai'))
        orderinfo.save()

        # 2 判断库存并创建详单对象
        for cid in cart_ids:
            cart = CartInfo.objects.get(id=cid)

            # 判断库存,库存大于购买
            if cart.count <= cart.goods.gkucun:
                # 减少库存
                cart.goods.gkucun -= cart.count
                # 保存！！
                cart.goods.save()
                # 创建详情信息
                detailinfo = OrderDetailInfo()
                detailinfo.goods = cart.goods
                detailinfo.order = orderinfo
                detailinfo.price = cart.goods.gprice
                detailinfo.count = cart.count
                detailinfo.save()
                # 删除购物车信息
                cart.delete()
            else:  # 库存小于购买
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'url': cid})  # 库存问题
        # 全部详情对象创建成功
        transaction.savepoint_commit(tran_id)
    except Exception as err:
        # 如果出现异常, 该订单不创建，跳转到用户中心我的订单
        print("{0}\n{1}".format('*'*10, err))
        transaction.savepoint_rollback(tran_id)

    return JsonResponse({'url': reverse('user:order')})

