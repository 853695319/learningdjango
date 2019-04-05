from django.shortcuts import render
from .models import BookInfo, HeroInfo

# HTTP的请求和响应，请求报文request封装好了，响应报文需要自己设置
# from django.http import HttpResponse
# from django.template import RequestContext, loader


def index(request):
    """
    :param request: HTTP请求
    :return: HTTP响应
    """
    # 加载模板
    # temp = loader.get_template('booktest/index.html')

    # 渲染页面
    # render_page = temp.render()  # render 渲染

    # 将内容返回给浏览器
    # return HttpResponse(render_page)

    # 一句话完成上面步骤
    # 从models取得数据
    bookList = BookInfo.objects.all()  # 取得全部图书对象

    # 将数据填入template
    context = {'list': bookList}
    return render(request, template_name='booktest/index.html', context=context)
