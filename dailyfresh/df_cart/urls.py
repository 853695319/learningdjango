from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.cart, name='cart'),
    # 默认添加-id商品-1件
    url(r'^add-(\d+)-(\d+)/$', views.add, name='add'),
    # 更新购物车件数
    url(r'^update-cart/$', views.update_cart, name='update_cart'),
    # 修改-cartID-数量
    url(r'^edit-(\d+)-(\d+)/$', views.edit, name='edit'),
    # 删除-cartID
    url(r'^delete-(\d+)', views.delete, name='delete'),
]
