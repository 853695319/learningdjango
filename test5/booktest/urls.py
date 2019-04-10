from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^error/$', views.view_error),
    url(r'^uploadpic/$', views.upload_pic),
    url(r'^uploadhandle/$', views.upload_handle),
    url(r'^paginator/(\S*)$', views.userlist),
]
