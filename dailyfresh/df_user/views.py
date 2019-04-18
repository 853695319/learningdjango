from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import hashlib
from django.http import HttpResponseRedirect
from .user_decorator import login_wrapper


# 注册
def register(request):
    context = {'title': '注册'}
    return render(request, 'df_user/register.html', context)


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

    # 转到用户登录界面登录
    return redirect('/user/login/')


def register_exit(request):
    user_name = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=user_name).count()
    return JsonResponse({'count': count})


# 登录
def login(request):
    if not request.POST:
        # 第一次 GET 方法渲染页面
        user_name = request.COOKIES.get('uname', '')
        context = {
            'title': '用户登录',
            'uname': user_name,

            # 和下面格式保持一致，如果不设置返回值，js会报错 if (==1) error
            'error_name': 0,
            'error_pwd': 0
        }
    else:
        # 接收请求
        post = request.POST
        uname = post.get('username')
        upwd = post.get('pwd')
        # 勾选了提交 1 ，不勾选就没这个key，设默认 0 不记住用户名
        jizhu = post.get('jizhu', 0)

        # 查询
        userlist = UserInfo.objects.filter(uname=uname)  # 不用get防止报错

        # 判断
        if len(userlist) == 1:
            sha1 = hashlib.sha1()
            sha1.update(upwd.encode())
            upwd_sha1 = sha1.hexdigest()

            if upwd_sha1 == userlist[0].upwd:
                # 加入登录验证后，用户登录后，跳转回登录前的操作页面，如购物车
                url = request.COOKIES.get('url', default='/')  # 默认跳转到主页
                redi = HttpResponseRedirect(url)

                # cookies记住用户名
                if jizhu != 0:
                    redi.set_cookie('uname', uname)
                else:
                    redi.set_cookie('uname', '', max_age=-1)  # 立刻过期

                # session记下常用信息
                request.session['user_id'] = userlist[0].id  # 可以用来判断用户是否已经登录
                request.session['uname'] = uname

                return redi
            else:
                context = {
                    'title': '用户登录',
                    'uname': uname,
                    'upwd': upwd,
                    'error_name': 0,
                    'error_pwd': 1  # 密码错误
                }

        else:
            context = {
                'title': '用户登录',
                'uname': uname,
                'upwd': upwd,
                'error_name': 1,  # 用户名错误
                'error_pwd': 0
            }

    return render(request, 'df_user/login.html', context)


# 该方法集成到login了
def login_handle(request):

    # 接收请求
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    # 勾选了提交 1 ，不勾选就没这个key，设默认 0 不记住用户名
    jizhu = post.get('jizhu', 0)

    # 查询
    userlist = UserInfo.objects.filter(uname=uname)  # 不用get防止报错

    # 判断
    if len(userlist) == 1:
        sha1 = hashlib.sha1()
        sha1.update(upwd.encode())
        upwd_sha1 = sha1.hexdigest()

        if upwd_sha1 == userlist[0].upwd:
            # 转到用户信息
            redi = HttpResponseRedirect('/user/info/')

            # cookies记住用户名
            if jizhu != 0:
                redi.set_cookie('uname', uname)
            else:
                redi.set_cookie('uname', '', max_age=-1)  # 立刻过期

            # session记下常用信息
            request.session['user_id'] = userlist[0].id
            request.session['uname'] = uname

            return redi
        else:
            context = {
                'title': '用户登录',
                'uname': uname,
                'upwd': upwd,
                'error_name': 0,
                'error_pwd': 1  # 密码错误
            }

    else:
        context = {
            'title': '用户登录',
            'uname': uname,
            'upwd': upwd,
            'error_name': 1,  # 用户名错误
            'error_pwd': 0
        }

    return render(request, 'df_user/login.html', context)


# 请求网址的时候进行验证
@login_wrapper
def info(request):
    user_id = request.session.get('user_id')
    userinfo = UserInfo.objects.get(id=user_id)
    context = {
        'title': '用户中心',
        'user_page': 1,
        'user_name': userinfo.uname,
        'user_email': userinfo.umail
    }
    return render(request, 'df_user/user_center_info.html', context)


@login_wrapper
def order(request):
    context = {
        'title': '用户中心',
        'user_page': 1,
    }
    return render(request, 'df_user/user_center_order.html', context)


@login_wrapper
def site(request):
    user_id = request.session.get('user_id')
    userinfo = UserInfo.objects.get(id=user_id)
    if request.method == 'POST':
        post = request.POST
        userinfo.ushou = post.get('ushou')
        userinfo.uaddress = post.get('uaddress')
        userinfo.uyoubian = post.get('uyoubian')
        userinfo.uphone = post.get('uphone')
        userinfo.save()

    context = {
        'title': '用户中心',
        'user': userinfo,
        'user_page': 1,
    }
    return render(request, 'df_user/user_center_site.html', context)
