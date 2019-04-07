from django.contrib import admin
from .models import BookInfo, HeroInfo


class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['btitle', 'bpub_date']


class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['hname', 'gender', 'hcontent', 'book']


admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
