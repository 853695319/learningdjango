from django.shortcuts import render
from .forms import *
from .models import *


def myeditor(request):
    # 如果这是一个POST请求,我们就需要处理表单数据
    if request.method == 'POST':
        # 创建一个表单实例,并且使用表单数据填充request请求:
        form = PostForm(request.POST)
        # 检查数据有效性:
        # Validate the form:
        # the captcha field will **automatically** check the input!!
        # 不区分大小写
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
