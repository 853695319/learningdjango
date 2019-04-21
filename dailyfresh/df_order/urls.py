from django.conf.urls import url
from . import views


urlpatterns = [
    # /order/?cartid=cartid&...
    url(r'^$', views.order, name='order'),
]
