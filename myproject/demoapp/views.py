from django.shortcuts import render
from django.http import JsonResponse
from .task import *


def celery_test(request):
    # 异步调用
    time_consuming_fun.delay()
    # 直接调用
    # time_consuming_fun()
    return JsonResponse({'msg': 'ok', 'code': 200})
