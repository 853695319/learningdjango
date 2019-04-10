from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'booktest/index.html')


def view_error(request):
    a1 = int('abc')
    return HttpResponse('hello')
