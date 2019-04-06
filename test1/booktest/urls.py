from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),

    # ([0-9]+) 取得匹配结果，所以showhero接收两个参数，request和book.id
    # 如果不加括号，就得不到id，只接收1个参数request
    url(r'^([0-9]+)$', views.showhero, name='showhero'),
]
