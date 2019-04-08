from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


def index(request):
    # return HttpResponse("hello world")
    return HttpResponse(request.path)  # HTTP请求路径,不包括域名！！


def detail(request, p1, p2, p3):
    return HttpResponse("p1:%s,p2:%s,p3:%s" % (p1, p2, p3))


# getTest1用于定义链接
def getTest1(request):
    return render(request, 'booktest/getTest1.html')


# getTest2用于接收一键一值
def getTest2(request):
    # 根据键接收值
    # a1 = request.GET['a']
    a1 = request.GET.get('a', 'NGET')  # 可以防止因键不存在出异常
    b1 = request.GET['b']
    c1 = request.GET['c']
    # 构建上下文
    context = {
        'a': a1,
        'b': b1,
        'c': c1,
    }
    # 向模板中传递上下文，并进行渲染
    return render(request, 'booktest/getTest2.html', context)


# getTest3用于接收一键多值
def getTest3(request):
    a1 = request.GET.get('a', 'NGET')  # 只接收最后一个
    a1 = request.GET.getlist('a', 'NGET')
    context = {'a': a1}
    return render(request, 'booktest/getTest3.html', context)


def postTest1(request):
    return render(request, "booktest/postTest1.html")


def postTest2(request):
    uname = request.POST.get('uname')
    upwd = request.POST.get('upwd')
    ugender = request.POST.get('ugender')
    uhobby = request.POST.getlist('uhobby')
    context = {
        'uname': uname,
        'upwd': upwd,
        'ugender': ugender,
        'uhobby': uhobby,
    }
    return render(request, "booktest/postTest2.html", context)


def cookieTest(request):
    """cookie 字典对象,基于域名隔离，不可跨域名，
    但可以嵌入其他网站也可以读取，例如淘宝<iframe>嵌在不同网站的广告"""
    response = HttpResponse()
    cookie = request.COOKIES  # 服务器接收cookie
    if 't1' in cookie:  # dict.has_key('key') 在python3已经废弃了，用 in 方法代替
        response.write(cookie['t1'])
    # response.set_cookie('t1', 'abc')  # 服务器发出cookie
    return response


# 重定向
def redirectTest1(request):
    # http://127.0.0.1:8000/booktest/redirectTest1/
    # return HttpResponseRedirect('/booktest/redirectTest2/')
    return redirect('/booktest/redirectTest2/')


def redirectTest2(request):
    return HttpResponse("重定向到这里redirectTest2")


# 通过用户登录练习session
# http://127.0.0.1:8000/booktest/sessionTest1/
def sessionTest1(request):
    uname = request.session.get('username', '陌生人')
    context = {'uname': uname}
    return render(request, 'booktest/sessionTest1.html', context)


def sessionTest2(request):
    return render(request, 'booktest/sessionTest2.html')


def sessionTest2_handle(request):
    uname = request.POST['uname']
    request.session['username'] = uname  # 启用session
    request.session.set_expiry(0)  # 如果value为0，那么用户会话的Cookie将在用户的浏览器关闭时过期
    return redirect('/booktest/sessionTest1/')


def sessionTest3(request):
    del request.session['username']  # 删除session
    return redirect('/booktest/sessionTest1')
