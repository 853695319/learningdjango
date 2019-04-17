from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail/$', views.goods_detail, name='goods-detail'),
    url(r'^list/$', views.gooods_list, name='goods-list'),
]
