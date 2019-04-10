from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
from .models import *
from django.core.paginator import *


def index(request):
    return render(request, 'booktest/index.html')


def view_error(request):
    a1 = int('abc')
    return HttpResponse('hello')


def upload_pic(request):
    # http://127.0.0.1:8000/uploadpic/
    return render(request, 'booktest/uploadpic.html')


def upload_handle(request):
    # https://yiyibooks.cn/xx/Django_1.11.6/ref/files/uploads.html#django.core.files.uploadedfile.UploadedFile
    pic1 = request.FILES['pic1']  # object: UploadedFile
    pic_name = os.path.join(settings.MEDIA_ROOT, pic1.name)  # UploadedFile.name
    with open(pic_name, 'wb') as destination:
        # 从网络流中读取文件
        for chunk in pic1.chunks():  # UploadedFile.chunks()
            destination.write(chunk)
    return HttpResponse(
        '<img src="/static/media/{}" alt="pic" style="width:30%">上传成功'.format(pic1.name)
    )


# 分页
def userlist(request, page_index):

    # 获取数据
    list = UserInfo.objects.all()

    # 数据分页，每页5个
    paginator = Paginator(list, 5)

    # 页码
    if not page_index:
        page_index = '1'

    page = paginator.page(int(page_index))

    context = {'page': page}
    return render(request, 'booktest/paginator.html', context)

