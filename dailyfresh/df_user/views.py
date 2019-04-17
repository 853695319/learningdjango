from django.shortcuts import render, redirect
from .models import *
import hashlib


def register(request):
    return render(request, 'df_user/register.html')


def register_handle(request):

    # 接收用户数据
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    # 判断用户密码
    if upwd != upwd2:
        return redirect('/user/register/')

    # 密码加密
    s1 = hashlib.sha1()
    s1.update(upwd.encode('utf-8'))
    upwd_sha1 = s1.hexdigest()

    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_sha1
    user.umail = uemail
    user.save()

    return render(request, 'df_user/login.html')


def login(request):
    return render(request, 'df_user/login.html')
