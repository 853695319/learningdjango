from django.contrib import admin
from .models import *


class UserInfoAdmin(admin.ModelAdmin):
    list_display = [
        'uname',
        'upwd',
    ]


admin.site.register(UserInfo, UserInfoAdmin)
