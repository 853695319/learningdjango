from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings


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
