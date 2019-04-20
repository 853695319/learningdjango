from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),

    # list分类-页码-排序
    url(r'^list(\d+)-(\d+)-(\d+)/$', views.goods_list, name='list'),
    url(r'^(\d+)/$', views.goods_detail, name='detail'),
]
