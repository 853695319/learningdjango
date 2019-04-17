from django.shortcuts import render
from .models import *


def index(request):
    # 查询分类最新4条，最热4条

    # 获取分类列表
    typelist = TypeInfo.objects.filter(isDelete=False)

    # 最新4条 一访问多：对象.模型类小写_set
    type_new0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    type_new1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    type_new2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    type_new3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    type_new4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    type_new5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]

    # 最热4条
    type_click0 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    type_click1 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type_click2 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type_click3 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type_click4 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type_click5 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    context = {
        # 模板继承
        'title': '首页',
        'goods_page': 1,
        'goods_index': 1,

        # 查询结果 最新
        'type_new0': type_new0,
        'type_new1': type_new1,
        'type_new2': type_new2,
        'type_new3': type_new3,
        'type_new4': type_new4,
        'type_new5': type_new5,

        # 最热
        'type_click0': type_click0,
        'type_click1': type_click1,
        'type_click2': type_click2,
        'type_click3': type_click3,
        'type_click4': type_click4,
        'type_click5': type_click5,
    }
    return render(request, 'df_goods/index.html', context)


def goods_detail(request):
    context = {
        # 模板继承
        'title': '商品详情',
        'goods_page': 1,
        'goods_index': 2
    }
    return render(request, 'df_goods/detail.html', context)


def gooods_list(request):
    context = {
        # 模板继承
        'title': '商品列表',
        'goods_page': 1,
        'goods_index': 2
    }
    return render(request, 'df_goods/list.html', context)
