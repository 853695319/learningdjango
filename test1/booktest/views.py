# from django.shortcuts import render
from django.http import HttpResponse
# HTTP的请求和响应，请求报文request封装好了，响应报文需要自己设置


def index(request):
    """
    :param request: HTTP请求
    :return: HTTP响应
    """
    return HttpResponse('<h1>Hello World</h1>')
