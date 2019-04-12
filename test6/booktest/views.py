from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from .forms import *
from .models import *


def myeditor(request):
    # 如果这是一个POST请求,我们就需要处理表单数据
    if request.method == 'POST':
        # 创建一个表单实例,并且使用表单数据填充request请求:
        form = PostForm(request.POST)
        # 检查数据有效性:
        if form.is_valid():
            # 获得数据
            data = form.cleaned_data['content']
            # 存入数据库
            mypost = Post()
            mypost.content = data
            mypost.save()
            # 到admin查看数据变化
            return render(request, 'booktest/showpost.html', {'data': data})  # {{ 'data'|safe }}

    # 如果是GET(第一次访问页面时)或者其它请求方法，我们将创建一个空的表单。
    else:
        myform = PostForm()
    return render(request, 'booktest/myeditor.html', {'myform': myform})


# 缓存
# @cache_page(60*10)  # timeout=60*10
def cache1(request):
    # return HttpResponse('hello1')

    # 在缓存过期前修改返回数据，看缓存是否有效
    # return HttpResponse('hello2')

    # 缓存数据
    # 设置缓存
    # cache.set('key1', 'value', 600)

    # 得到缓存
    # print('\ncache.get:'+cache.get('key1')+'\n')
    # return render(request, 'booktest/cache1.html')

    # 清空redis缓存
    cache.clear()
    return HttpResponse('cache clear')


def mysearch(request):
    return render(request, 'booktest/mysearch.html')
