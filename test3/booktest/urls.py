from django.conf.urls import url
from . import views

urlpatterns = {
    url(r'^$', views.index, name='index'),  # http://127.0.0.1:8000/booktest/
    # url(r'^(\d+)/(\d+)/(\d+)$', views.detail, name='detail'),  # http://127.0.0.1:8000/booktest/2019/4/7
    url(r'^(?P<p2>\d+)/(?P<p3>\d+)/(?P<p1>\d+)$', views.detail, name='detail'),  # http://127.0.0.1:8000/booktest/2019/4/7

    # GET
    url(r'^getTest1/$', views.getTest1),
    url(r'^getTest2/$', views.getTest2),
    url(r'^getTest3/$', views.getTest3),

    # POST
    url(r'^postTest1/$', views.postTest1),
    url(r'^postTest2/$', views.postTest2),

    # cookie
    url(r'^cookieTest/$', views.cookieTest),

    # redirect
    url(r'^redirectTest1/$', views.redirectTest1),
    url(r'^redirectTest2/$', views.redirectTest2),

    # session
    url(r'^sessionTest1/$', views.sessionTest1),
    url(r'^sessionTest2/$', views.sessionTest2),
    url(r'^sessionTest2_handle/$', views.sessionTest2_handle),
    url(r'^sessionTest3/$', views.sessionTest3),
}