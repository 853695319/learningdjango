from django.shortcuts import render, redirect
from .models import *
from .user_decorator import login_wrapper
from django.http import JsonResponse
from django.urls import reverse


@login_wrapper
def cart(request):
    """渲染购物车界面"""
    # 查询对应用户的购物车
    uid = request.session.get('user_id')
    cart_set = CartInfo.objects.filter(user_id=uid)

    context = {
        # 模板继承
        'title': '购物车',
        'user_page': 1,

        'cart_set': cart_set,
    }
    return render(request, 'df_cart/cart.html', context)


@login_wrapper
def add(request, gid, count):
    """增加特定商品数量"""
    # 查询对应用户购物车里是否有给商品
    uid = request.session.get('user_id')
    cart_set = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    count = int(count)
    # 添加商品到购物车
    if cart_set.count() > 0:
        gid_cart = cart_set[0]
        gid_cart.count += count
    else:
        gid_cart = CartInfo()
        gid_cart.user_id = uid
        gid_cart.goods_id = gid
        gid_cart.count = count
    # 保存到数据库
    gid_cart.save()

    # 如果不是ajax则跳转到购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'count': count})
    else:
        return redirect(reverse('df_cart:cart'))


def update_cart(request):
    """更新我的购物车商品件数"""
    uid = request.session.get('user_id', '')
    if not uid:
        count = 0
    else:
        count = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'count': count})


@login_wrapper
def edit(request, cart_id, count):
    """通过ajax修改购物车商品数量"""
    try:
        cartinfo = CartInfo.objects.get(id=int(cart_id))
        cartinfo.count = int(count)
        cartinfo.save()
        data = {'ok': 0}
    except Exception as err:
        data = {'ok': int(count)}
    return JsonResponse(data)
