from django.conf.urls import url
from . import views


urlpatterns = [
    # GET /order/?cartid=cartid&...
    url(r'^$', views.order, name='order'),
    # POST
    url(r'^handle/$', views.order_handle, name='handle'),
]
