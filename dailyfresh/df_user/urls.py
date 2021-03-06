from django.conf.urls import url
from . import views


urlpatterns = [
    # 注册
    url(r'^register/$', views.register, name='register'),
    url(r'^register-handle/$', views.register_handle, name='register-handle'),
    url(r'^register-exit/$', views.register_exit, name='register-exit'),
    # login
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    # 用户中心
    url(r'^info/$', views.info, name='info'),
    url(r'^site/$', views.site, name='site'),
    url(r'^order(?:(\d+))?/$', views.order, name='order'),
]
