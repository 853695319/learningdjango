from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register-handle/$', views.register_handle),
    url(r'^login/$', views.login),
]
