from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),

    # list分类-页码-排序
    url(r'^list(\d+)-(\d+)-(\d+)/$', views.goods_list, name='list'),
    url(r'^(\d+)/$', views.goods_detail, name='detail'),

    # 全文检索 模板继承
    # 2.4.0
    # url(r'^search/?$', views.MySearchView()),
    # 2.7.0
    url(r'^search/?$', views.JohnSearchView.as_view(), name='haystack_search'),
]

