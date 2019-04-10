from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(\d+)/$', views.show, name='show'),

    # 模板继承
    # 基于base.html
    url(r'^index2/$', views.index2, name='index2'),

    # base_user.html
    url(r'^user1/$', views.user1, name='user1'),
    url(r'^user2/$', views.user2, name='user2'),

    # html转义
    url(r'^htmlTest/$', views.htmlTest, name='htmlTest'),

    # csrf
    url(r'^csrf1/$', views.csrf1, name='csrf1'),
    url(r'^csrf2/$', views.csrf2, name='csrf2'),

    # 验证码
    url(r'^captcha/$', views.generateCaptcha, name='generateCaptcha'),
    url(r'^showcaptcha/$', views.showcaptcha, name='showcpatcha'),
    url(r'^verifyCode/$', views.verifyCode, name='verifyCode'),

    # django-simple-captcha
    url(r'^testcaptcha/$', views.get_captcha, name='get_captcha'),
]
