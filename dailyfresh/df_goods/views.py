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


def goods_detail(request, new_id):

    # 查询商品
    good = GoodsInfo.objects.get(id=int(new_id))

    # 纪录点击量
    good.gclick += 1
    good.save()  # 记得保存！！

    # 推荐商品
    news = GoodsInfo.objects.filter(gtype_id=good.gtype_id).order_by('-id')[:2]

    context = {
        # 模板继承
        'title': good.gtitle,
        'goods_page': 1,
        'goods_index': 2,

        # 商品详情
        'good': good,
        'type': good.gtype,
        'news': news,
        'initnum': '1',
    }
    response = render(request, 'df_goods/detail.html', context)

    # 可以改进，通过session判断该用户是否已经登录，如果登录了，就给他提供最经浏览
    # 在cookie加盐，盐为user_id，这样就可以实现对应用户看对应的信息了吧
    # 不然同一浏览器浏览后，别人再上号，会看到其他人的记录
    # 但是同一个cookie['view_list'],也会被别人的记录覆盖，上一个人的记录就不见了
    user_id = request.session.get('user_id', '')
    if not user_id:
        return response

    # 记住用户最近浏览
    new_id = "%d" % good.id

    # 从cookies中获取最近浏览
    key = 'view_list_{}'.format(user_id)
    view_list = request.COOKIES.get(key, '')
    # view_list = request.get_signed_cookie('view_list', default='', salt=str(user_id))

    if view_list == '':
        view_list = new_id  # 浏览记录为空，直接添加
    else:
        # 分割成列表
        good_id_list = view_list.split(',')

        # 如果商品已经记录，则删除，并将该商品添加到第一个位！
        if new_id in good_id_list:
            good_id_list.remove(new_id)
        good_id_list.insert(0, new_id)

        # 如果列表长度大于6，删除最后一个
        if len(good_id_list) > 5:
            good_id_list.pop()
        # 拼接成字符串
        view_list = ','.join(good_id_list)

    response.set_cookie(key, view_list)
    # response.set_signed_cookie('view_list', view_list, salt)
    return response


def goods_list(request, type_id, page_num, sort_id):

    # 分类信息
    good_type = TypeInfo.objects.get(id=int(type_id))

    # 新品推荐
    goods_new = good_type.goodsinfo_set.order_by('-id')[0:2]

    # UnboundLocalError: local variable 'x' referenced before assignment
    goodslist = []
    if sort_id == '1':  # 默认 最新 sort_id = string
        goodslist = good_type.goodsinfo_set.order_by('-id')
    elif sort_id == '2':  # 价格降序
        goodslist = good_type.goodsinfo_set.order_by('-gprice')
    elif sort_id == '3':  # 点击量
        goodslist = good_type.goodsinfo_set.order_by('gclick')

    # 分页
    paginator = Paginator(goodslist, 10)

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


from haystack.views import SearchView as SearchView240  # 2.4.0以前的 page


class MySearchView(SearchView240):
    """补充模板上下文对象实现模板继承"""
    def extra_context(self):
        # 继承
        extra = super(MySearchView, self).extra_context()
        # 补充上下文
        extra['title'] = '搜索'
        extra['goods_page'] = 1
        extra['goods_index'] = 2
        return extra


from haystack.generic_views import SearchView  # 2.4.0 以后 模板上最大的不同在于page-> page_obj


class JohnSearchView(SearchView):
    template_name = 'search/search-new.html'

    def get_context_data(self, *args, **kwargs):
        extra = super(JohnSearchView, self).get_context_data(*args, **kwargs)
        # 补充上下文
        extra['title'] = '搜索'
        extra['goods_page'] = 1
        extra['goods_index'] = 2
        return extra
