from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^celerytest/$', views.celery_test),
]