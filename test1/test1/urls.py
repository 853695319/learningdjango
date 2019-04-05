"""test1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

# Add an import:  from my_app import views 按要求写导入，不用担心报错！！
# from booktest import views


urlpatterns = [
    # include 写法，就是会去引入那个路径的urls (Including another URLconf)
    # r'^admin/' 匹配 admin/...
    url(r'^admin/', include(admin.site.urls)),

    # r'^$' 其实就是正则，匹配空，就相当于进入 view.index
    # url(r'^$', views.index, name='index'),

    # include 写法,关键在用单引号将 booktest.urls 引起来
    url(r'^', include('booktest.urls'))
]
