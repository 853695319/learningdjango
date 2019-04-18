from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator


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


def goods_detail(request, good_id):
    context = {
        # 模板继承
        'title': '商品详情',
        'goods_page': 1,
        'goods_index': 2
    }
    return render(request, 'df_goods/detail.html', context)


def gooods_list(request, type_id, page_num, sort_id):

    # 分类信息
    good_type = TypeInfo.objects.get(id=int(type_id))

    # 新品推荐
    goods_new = good_type.goodsinfo_set.sort('-id')[0:2]
    if sort_id == 1:  # 默认 最新
        goods_list = good_type.goodsinfo_set.order_by('-id')
    elif sort_id == '2':  # 价格降序
        goods_list = good_type.goodsinfo_set.order_by('-gprice')
    elif sort_id == '3':  # 点击量
        goods_list = good_type.goodsinfo_set.order_by('gclick')

    # 分页
    paginator = Paginator(goods_list, 10)

    # 取得相应页的内容
    page = paginator.page(int(page_num))

    context = {
        # 模板继承
        'title': '商品列表',
        'goods_page': 1,
        'goods_index': 2,

        # 商品列表
        'page': page,
        'paginator': paginator,
        'good_type': good_type,
        'sort_id': sort_id,
        'goods_new': goods_new
    }
    return render(request, 'df_goods/list.html', context)
