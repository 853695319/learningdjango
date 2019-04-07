from django.shortcuts import render
from django.db.models import Max, F
from .models import BookInfo


def index(request):
    """"""
    # context={'list': BookInfo.book1.filter(heroinfo__hcontent__contains='八')}
    # _list = BookInfo.book1.aggregate(Max('bpub_date'))  # 不是列表,是字典！！
    _list = BookInfo.book1.filter(bread__lt=F('bcomment'))  # 阅读量小于评论量
    context = {'list': _list}
    return render(request, 'booktest/index.html', context)
