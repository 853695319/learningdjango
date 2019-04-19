from django.conf.urls import url
from . import views


urlpatterns = [
    # 注册
    url(r'^register/$', views.register),
    url(r'^register-handle/$', views.register_handle),
    url(r'^register-exit/$', views.register_exit),
    # login
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^info/$', views.info),
    url(r'^order/$', views.order),
    url(r'^site/$', views.site)
]
