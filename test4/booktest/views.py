from django.shortcuts import render
from .models import *


def index(request):
    # hero = HeroInfo.objects.get(pk=1)
    # context = {'hero': hero}

    # herolist= HeroInfo.objects.filter(idDelete=True)  # 测试 {% empty %}
    herolist = HeroInfo.objects.all()
    context = {'herolist': herolist}
    return render(request, 'booktest/index.html', context)


def show(request, id_):
    context = {'id': id_}
    return render(request, 'booktest/show.html', context)


# 模板继承
def index2(request):
    return render(request, 'booktest/index2.html')


def user1(request):
    context = {'uname': 'user1.html'}  # 那么这个变量可以用在 user.html,它的父模板也是可以用这个变量的
    return render(request, 'booktest/user1.html', context)


def user2(request):
    return render(request, 'booktest/user2.html')
