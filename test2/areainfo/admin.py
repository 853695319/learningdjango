from django.contrib import admin
from .models import AreaInfo


class AreaInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'atitle', 'aparent']


admin.site.register(AreaInfo, AreaInfoAdmin)
