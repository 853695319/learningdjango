from django.contrib import admin
# python3 包的相对导入
from .models import BookInfo, HeroInfo


# class HeroInfoInline(admin.StackedInline):
#     """
#     关联类： 建立与图书的关联
#     层叠效果
#     """
#     model = HeroInfo
#     # 在增加图书信息时，可以而外嵌入3个英雄信息
#     extra = 3


class HeroInfoInline(admin.TabularInline):
    """
    关联类： 建立与图书的关联
    表格效果
    """
    model = HeroInfo
    # 在增加图书信息时，可以而外嵌入3个英雄信息
    extra = 3


class BookInfoAdmin(admin.ModelAdmin):
    """定义BookInfo在网页的显示"""
    # 展示页
    # list_display = ['id', 'btitle', 'bpub_date']
    list_display = ['btitle', 'bpub_date']  # 显示字段
    list_filter = ['btitle']  # 过滤
    search_fields = ['btitle']  # 搜索栏
    # list_per_page = 1  # 分页
    # 修改页
    fieldsets = [
        ('base', {'fields': ['btitle']}),
        ('super', {'fields': ['bpub_date']})
    ]
    # 嵌入关联
    inlines = [HeroInfoInline]


class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['hname', 'gender', 'hcontent', 'hbook']


admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
# Register your models here.

