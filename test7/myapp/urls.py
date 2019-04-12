from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^mysearch/$', views.mysearch, name='mysearch'),
]