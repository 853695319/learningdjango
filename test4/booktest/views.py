from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *


def index(request):
    # hero = HeroInfo.objects.get(pk=1)
    # context = {'hero': hero}

    # herolist= HeroInfo.objects.filter(idDelete=True)  # 测试 {% empty %}
    herolist = HeroInfo.objects.all()
    context = {'herolist': herolist}
    return render(request, 'booktest/index.html', context)


def show(request, id_):
    context = {'id': id_}
    return render(request, 'booktest/show.html', context)


# 模板继承
def index2(request):
    return render(request, 'booktest/index2.html')


def user1(request):
    context = {'uname': 'user1.html'}  # 那么这个变量可以用在 user.html,它的父模板也是可以用这个变量的
    return render(request, 'booktest/user1.html', context)


def user2(request):
    return render(request, 'booktest/user2.html')


# html转义
def htmlTest(request):
    context = {'html': '<h1>123</h1>'}
    return render(request, 'booktest/htmlTest.html', context)


# csrf
def csrf1(request):
    return render(request, 'booktest/csrf1.html')


def csrf2(request):
    uname = request.POST['uname']
    return HttpResponse(uname)


# 验证码
def generateCaptcha(request):
    """
    生成验证码图片，存放到内存
    关键是使用MIME格式，体会如何利用第三方库编程
    """
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 创建背景色RGB
    bgColor = (
        random.randrange(50, 100),  # R
        random.randrange(50, 100),  # B
        0,  # G
    )

    # 规定宽高
    width = 100
    height = 25

    # 创建画布
    image = Image.new('RGB', (width, height), bgColor)

    # 创建画笔
    draw = ImageDraw.Draw(image)

    # 创建文本内容
    # ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”,他会自己去找
    font = ImageFont.truetype('FreeMono.ttf', 24)
    # text = 'ABCD'  # 简单测试
    text_dict = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'  # 定义验证码的备选值
    text_temp = ''
    # 将字符逐一绘制到画布
    for i in range(4):
        text_temp += text_dict[random.randrange(0, len(text_dict))]
        draw.text(
            xy=(i*25, 0),  # 字母均匀分布
            # random.randrange 不包括 endpoint -> len(text_dict)
            text=text_temp[-1],
            fill=(255, 255, 255),
            font=font
        )

    # KeyPoint:将验证码写入session保存到服务器，不直接放到cookie上，注意隐私
    request.session['captcha'] = text_temp

    # 将内容绘制在画布上
    # draw.text(xy=(0, 0), text=text, fill=(255, 255, 255), font=font)
    # 注意把参数名写上，第三个位置是fill，不写上参数名就把font放在第三位，会报错！！
    # draw.text(xy=(0, 0), text=text, font=font)

    # 将图像保存到内存流中
    import io
    buf = io.BytesIO()
    # Image.save(fp, format=None, **params)
    # 如果 fp是一个对象，该对象需要有write方法，且以二进制方式写入
    image.save(buf, 'png')

    # 将内存流中的内容输出到客户端，重点：注意使用MIME类型
    return HttpResponse(buf.getvalue(), 'image/png')


def showcaptcha(request):
    """渲染带有验证码的表单页"""
    return render(request, 'booktest/showcaptcha.html')


def verifyCode(request):
    """接收表单输入的验证码，验证是否正确"""
    # 接收POST输入
    recv_code = request.POST.get('recv_code')

    # 取session中的captcha
    captcha = request.session.get('captcha')

    # 比较
    if captcha == recv_code:
        return HttpResponse('Successful')
    else:
        return render(request, 'booktest/showcaptcha.html', {'statu': 'Try again'})


def get_captcha(request):
    """
    利用django-simple-captcha库生成验证码
    http://127.0.0.1:8000/testcaptcha/
    """
    from .forms import CaptchaTestForm
    # 如果这是一个POST请求,我们就需要处理表单数据
    if request.method == 'POST':
        # 创建一个表单实例,并且使用表单数据填充request请求:
        form = CaptchaTestForm(request.POST)
        # 检查数据有效性:
        # Validate the form:
        # the captcha field will **automatically** check the input!!
        # 不区分大小写
        if form.is_valid():
            your_name = form.cleaned_data['your_name']
            # return redirect('/thanks/')
            return HttpResponse('Hello %s' % your_name)

    # 如果是GET(第一次访问页面时)或者其它请求方法，我们将创建一个空的表单。
    else:
        form = CaptchaTestForm()

    return render(request, 'captcha/testcaptcha.html', {'form': form})
