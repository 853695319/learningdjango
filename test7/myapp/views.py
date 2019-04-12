from django.shortcuts import render
from .task import *
from django.http import HttpResponse


# 全文检索
def mysearch(request):
    return render(request, 'myapp/mysearch.html')


# celery 异步
def celery_test(request):
    # sayhello()
    sayhello.delay()
    return HttpResponse('task-sayhello: ok')
