from django.shortcuts import render, redirect
from .models import *
from .user_decorator import login_wrapper


@login_wrapper
def cart(request):
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


def add(request):
    return
