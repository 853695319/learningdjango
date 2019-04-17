from django.contrib import admin
from .models import *


class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'ttitle']


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'gtitle', 'gprice', 'gunit', 'gclick', 'gkucun'
    ]


admin.site.register(TypeInfo, TypeInfoAdmin)
admin.site.register(GoodsInfo, GoodsInfoAdmin)

# superuser: root qew96898
