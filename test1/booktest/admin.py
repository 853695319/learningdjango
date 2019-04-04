from django.contrib import admin
# python3 包的相对导入
from .models import BookInfo, HeroInfo


class BookInfoAdmin(admin.ModelAdmin):
    """定义BookInfo在网页的显示"""
    # 展示页
    list_display = ['id', 'btitle', 'bpub_date']
    list_filter = ['btitle']
    search_fields = ['btitle']
    list_per_page = 1
    # 修改页
    fieldsets = [
        ('base', {'fields': ['btitle']}),
        ('super', {'fields': ['bpub_date']})
    ]


admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo)
# Register your models here.

