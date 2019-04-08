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
