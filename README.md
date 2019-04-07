# learningdjango
记录学习django的过程资料

django_py3.6 python3.6虚拟环境
test1 是django项目文件夹




# Django-开发流程





## Django-搭建开发环境
### 创建python3虚拟环境
```
python3 -m venv /path/to/new/virtual/environment
```
在 **~/09-django/learningdjango** 目录下！！
```
python3 -m venv django_py3.6
```
* 删除虚拟环境

由于venv创建的是一个轻量级虚拟环境，直接删除对应的文件夹 django_py3.6就可以了

`rm -r django_py3.6`
* 进入虚拟环境
```markdown
source <venv>/bin/activate

source django_py3.6/bin/activate
```
* 退出虚拟环境
You can deactivate a virtual environment by typing “deactivate” in your shell
`deactivate`

### 安装django

建议安装1.8.2版本，这是一个稳定性高、使用广、文档多的版本

`pip install django==1.8.2`

查看版本：进入python shell，运行如下代码
```
import django
django.get_version()
```
说明：使用pip install django命令进行安装时，会自动删除旧版本，再安装新版本







## Django-建立应用booktest 模型models 测试
* 创建项目

`django-admin startproject test1`

* 创建应用模块

在test1项目文件夹下创建booktest模块
```
python manage.py startapp booktest
```
* 在 models.py 定义模型类
```python
# booktest.models.py

from django.db import models

# Create your models here.

class BookInfo(models.Model):
    """图书结构"""
    # 定义类属性，是为了映射数据库中的相应字段，通过类创建的实例对象是不能操作类属性的
    # 类属性生成表结构的依据
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField()

    def __str__(self):
        return self.btitle
        # return self.btitle.encode('utf-8') 可能跟版本有关，视频里需要设置编码，而为这个版本要求string not byte


class HeroInfo(models.Model):
    """英雄结构"""
    hname = models.CharField(max_length=10)
    hgender = models.BooleanField()
    hcontent = models.CharField(max_length=1000)
    # 引入外键
    hbook = models.ForeignKey(BookInfo)

    def __str__(self):
        return self.hname

"""
In [1]: class Person(object):
   ...:     name = 'Person'
   ...:     def __str__(self):
   ...:         return self.name
   ...:     

In [2]: p = Person()

In [3]: p.name = 'p'

In [4]: print(p)
p

In [5]: Person.name
Out[5]: 'Person'

同理，下面这个也没错，类属性并没有被修改，是用来映射数据库字段的
from booktest.models import *
b = BookInfo()
b.btitle = 'abc'
为什么一定要用相同的属性名呢？
b.save()
调用save方法的时候类似 SQL INSERT 方法，将数据插入对应的字段中,所以属性名一定要一样
不用担心修改到类属性
"""

```
定义模型类后，可以到 test1项目文件夹下进行测试
```
python manage.py runserver 8080
```
* 注册应用模块(重要)

但实际并没有用到你刚刚做到，你需要先进行 迁移 应用
把应用注册到 /test1/test1/settings.py INSTALLED_APPS
```markdown
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 注册应用到setting.py，第三方包也要注册在这里
    'booktest',
)
```

* 生成迁移
```markdown
python manage.py makemigrations

Migrations for 'booktest':
  0001_initial.py:
    - Create model BookInfo
    - Create model HeroInfo
```
在 test1/booktest/migrations/0001_initial.py
可以看到相应的变化，里面为将来生产SQL语句作准备

* 执行迁移
```markdown
python manage.py migrate

Operations to perform:
  Synchronize unmigrated apps: staticfiles, messages
  Apply all migrations: admin, auth, contenttypes, sessions, booktest
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
  Installing custom SQL...
Running migrations:
  Rendering model states... DONE
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying booktest.0001_initial... OK
  Applying sessions.0001_initial... OK
```

* 测试数据操作
```markdown
python manage.py shell
```
* 新建图书信息
```
from booktest.models import *
b = BookInfo()
b.btitle = 'abc'
from datetime import datetime
b.bpub_date = datetime(year=1990, month=1, day=12)
b.save()

74: RuntimeWarning: DateTimeField BookInfo.bpub received a naive datetime (1990-01-12 00:00:00) while time zone support is active.
  RuntimeWarning)
```
时区问题，django默认给我们设置了时区，如果我们美设置的话
可以在 test1/test1/settings.py TIME_ZOME = 'UTC'

* 查找所有图书信息
```
BookInfo.objects.all()

[<BookInfo: BookInfo object>, <BookInfo: BookInfo object>]
```

添加方法 ```BookInfo.__str__()```
这个时候没有改变 模型的数据结构，所以不用重新迁移
应该重新开启shell，重载BookInfo
```
from booktest.models import *
BookInfo.objects.all()

[<BookInfo: abc>, <BookInfo: abc>]
```
* 修改图书内容
其中 pk is primary key.
```markdown
>>> b1 = BookInfo.objects.get(pk=1)
>>> b1.btitle
'abc'
>>> b1.btitle = '123'
>>> BookInfo.objects.all()
[<BookInfo: abc>, <BookInfo: abc>]
>>> b1.save()
>>> BookInfo.objects.all()
[<BookInfo: 123>, <BookInfo: abc>]
```
* 删除图书
物理上删除
```markdown
>>> b1.delete()
>>> BookInfo.objects.all()
[<BookInfo: abc>]
```






## Django-管理站点

* 创建一个管理员用户
```markdown
python manage.py createsuperuser，按提示输入用户名、邮箱、密码

username:abc
password:123
email:abc@163.com
```
* 运行web服务 默认端口：8000
```markdown
python manage.py runserver
```
通过http://127.0.0.1:8000/admin进入管理界面

* 本地化
```markdown
# test1/setting.py

LANGUSGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```
* 向admin注册booktest的模型
test1/booktest/admin.py
```
# booktest/admin.py

from django.contrib import admin

# python3 包的相对导入
from .models import BookInfo, HeroInfo


admin.site.register(BookInfo)
admin.site.register(HeroInfo)
```
* 修改后台管理admin网页
```markdown
# booktest/admin.py
from django.contrib import admin
# python3 包的相对导入
from .models import BookInfo, HeroInfo


class BookInfoAdmin(admin.ModelAdmin):
    """定义BookInfo在网页的显示"""
    # 列表页的显示样式
    list_display = ['id', 'btitle', 'bpub_date']
    list_filter = ['btitle']
    search_fields = ['btitle']
    list_per_page = 1
    # 添加、修改页的显示样式
    fieldsets = [
        ('base', {'fields': ['btitle']}),
        ('super', {'fields': ['bpub_date']})
    ]


admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo)

```
* 关联注册

可以实现在添加图书信息时，同时添加关联的英雄信息
```markdown
# booktest/models.py
from django.contrib import admin
from models import BookInfo,HeroInfo

# StackedInline 可以替换为 TabularInline 表格显示
class HeroInfoInline(admin.StackedInline):
    model = HeroInfo
    extra = 2

class BookInfoAdmin(admin.ModelAdmin):
    # 嵌入列表
    inlines = [HeroInfoInline]

admin.site.register(BookInfo, BookInfoAdmin)

```
* 布尔值显示
```markdown
# booktest/admin.py

class HeroInfo(models.Model):
    """英雄结构"""
    hname = models.CharField(max_length=10)
    hgender = models.BooleanField()
    hcontent = models.CharField(max_length=1000)
    # 引入外键
    hbook = models.ForeignKey(BookInfo)

    def __str__(self):
        return self.hname

    def gender(self):
        """布尔值显示性别"""
        if self.hgender:
            return "男"
        else:
            return "女"

    gender.short_description = '性别'

# booktest/admin.py

class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['hname', 'gender', 'hcontent', 'hbook']
    
admin.site.register(HeroInfo, HeroInfoAdmin)

```
这样修改后，点击`性别`这个字段，就没有排序功能了






## Django-视图view.py
* 定义视图
```markdown
# booktest/views.py
from django.http import HttpResponse
# HTTP的请求和响应，请求报文request封装好了，响应报文需要自己设置


def index(request):
    """
    :param request: HTTP请求 
    :return: HTTP响应
    """
    return HttpResponse('Hello World')
```
* 配置路由

基本上django的设置都在setting.py内完成

`ROOT_URLCONF = 'test1.urls'`

路由配置独立出来 `urls.py`
```
# test1/urls.py
from django.conf.urls import include, url
from django.contrib import admin

# Add an import:  from my_app import views 按要求写导入，不用担心报错！！
# from booktest import views


urlpatterns = [
    # include 写法，就是会去引入那个路径的urls (Including another URLconf)
    # r'^admin/' 匹配 admin/...
    url(r'^admin/', include(admin.site.urls)),

    # r'^$' 其实就是正则，匹配空，就相当于进入 view.index
    # url(r'^$', views.index, name='index'),

    # include 写法,关键在用单引号将 booktest.urls 引起来
    url(r'^', include('booktest_urls')),
]

# booktest/urls.py

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
]

```
可能遇到的异常：导入时编辑器提示异常，不用理他，按要求写导入，即便没有自动补全提示

**urls原理：**

假设域名：`www.itcast.com/...`

MVT会将`...`部分取出，用于路由匹配

`url(r'^admin/', include(admin.site.urls))`

先匹配 `admin/`，然后到 `admin.site.urls` 继续匹配





## Django-模板templates
* 定义模板

新建目录`templates/my_app/xxx.html`

注意`my_app`与应用模块同名！！

所以我的目录为`test1/templates/booktest/index.html`

* 添加模板路径
```markdown
# test1/setting.py

# os.path.join(path, *path) --> 到这个目录下BASE_DIR/templates/ 查找模板
# os.path.join('c:\\', 'csv', 'test.csv') --> 'c:\\csv\\test.csv' 
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```

* 添加模板
```markdown
# booktest/views.py

from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import RequestContext, loader


def index(request):
    """
    :param request: HTTP请求
    :return: HTTP响应
    """
    # 1 加载模板 注意路径的写法
    # temp = loader.get_template('booktest/index.html')

    # 2 渲染页面
    # render_page = temp.render()  # render 渲染

    # 3 将内容返回给浏览器
    # return HttpResponse(render_page)
    
    # 一句话完成上面步骤
    return render(request, template_name='booktest/index.html')
```
* views从models取得数据填入template中
```markdown
# booktest/views.py

from django.shortcuts import render
from .models import BookInfo, HeroInfo

def index(request):
    # 从models取得数据
    bookList = BookInfo.objects.all()  # 取得全部图书对象
    context = {'list': bookList}

    # 将数据填入template
    return render(request, template_name='booktest/index.html', context=context)



# templates/booktest/index.html

<ul>
    {%for book in list%}
    <li>{{book.btitle}}</li>
    {%endfor%}
</ul>
```

## Django-生成英雄展示页面
* index.html设置链接
```markdown
<li><a href="{{book.id}}">{{book.btitle}}</a></li>
```
* views初步定义函数
```markdown
# booktest/views.py

def showhero(request, book_id):
    hero_context = {}
    return render(request, 'booktest/showhero.html', hero_context)

```
* template初步定义模板

为测试链接是否能正确跳转到showhero.html

* 配置路由URLs
```markdown
# booktest/urls.py

# 为获取图书ID， ([0-9]+) 取得匹配结果，所以showhero接收两个参数，request和book.id
# 如果不加括号，就得不到id，只接收1个参数request
url(r'^([0-9]+)$', views.showhero, name='showhero'),

```
测试链接跳转

* 进一步完善views.showhero函数
```markdown
# booktest/views.py

def showhero(request, book_id):
    """
    :param request: HTTP请求
    :param book_id: 图书的ID
    :return: HTTP响应页面
    """
    # 1.要知道展示那本书
    book = BookInfo.objects.get(pk=book_id)
    
    # 2.该书对应的所有英雄对象集合 注意用all()方法获得可遍历列表[]
    hero_list = book.heroinfo_set.all()
    hero_context = {'list': hero_list}
    return render(request, 'booktest/showhero.html', hero_context)
```
可能遇到异常，提示```'RelatedManager' object is not iterable'```,
检查下自己有没有，用`all()`方法获得列表
* 进一步完善模板

## Django-总结开发流程

1. 定义models类，生成迁移，生成迁移是为了生成表结构,执行迁移
2. 启用管理站点admin，要先把models注册到admin，然后添加一些数据上去，作测试
3. 定义views,为了视图函数能被调用，需要配置URLs来匹配用户输入的网址
4. 定义templates，是为了呈现数据
5. views从models获得数据，把上下文context填入template，呈现网页

PS：

models.py定义的数据库只适用于**关系型数据库**，像Mongodb不适用；

主要重复过程：定义模型类，定义视图，配置URLs，创建模板



# MVT框架
对MVT的三大块进行学习
## MVT-模型models
```markdown
django-admin startproject test2
```
另外开启项目test2进行学习
### 创建基于Docker的Mysql
一开始用不到，开始用Django默认数据库 SQLite
```
docker run --name mysql-data \
           -p 8080:3306 \
           -v /home/chenzhixiong/09-django/learningdjango/mysqldata/myconfig:/etc/mysql/mysql.conf.d \
           -v /var/lib/mysql:/var/lib/mysql \
           -e MYSQL_ROOT_PASSWORD="root" \
           -d mysql:5.7 \
           --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```
* 问题1：
`ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)`

* 问题2：
莫名其妙的自动退出

一步步测试
```
docker run --name mysql-1 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:5.7
```
登录mysql
```
mysql -u root -p my-secret-pw
```

```
docker run -p 8080:3306 --name mysql-1 -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7
```
测试远程连接需要用宿主机的IP地址，而不是容器里面的IP地址！
```
docker run -p 8080:3306 --name mysql-1 -v /home/chenzhixiong/09-django/learningdjango/mysqldata/myconfig:/etc/mysql/mysql.conf.d -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7
```
成功映射配置
```
docker run -p 8080:3306 --name mysql-data -v /home/chenzhixiong/09-django/learningdjango/mysqldata/myconfig:/etc/mysql/mysql.conf.d -v /home/chenzhixiong/09-django/learningdjango/mysqldata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -d mysql:5.7
```
开启不了

最终可用版
```
docker run -p 8080:3306 --name mysql-data -v /home/chenzhixiong/09-django/learningdjango/myconfig:/etc/mysql/mysql.conf.d -v /home/chenzhixiong/09-django/learningdjango/mysqldata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -it mysql:5.7
```
说明：

* -p 挂载端口
* -v 映射目录
* -e MYSQL_ROOT_PASSWORD=root 环境变量，官方给出的，设置初始root密码
* 我在这里把配置文件挂到`/etc/mysql/mysql.conf.d `这个目录，其实不太对因为这个目录里的好像是默认配置文件的模板，实际应该用`/etc/mysql/my.cnf`
    


意外发现，被docker挂载后的文件夹会被docker改变权限，只有docker用得了，我要用 chmod a+rwx -R * 修改权限才能使用
所以以后docker挂载的目录应设置号具体地方，不要和本地数据库共用同一目录





### 使用MySQL数据库
* 在虚拟环境中安装mysql包
```markdown
pip3 install mysql-python
```
* 在mysql中创建数据库

我们在模型类中进行迁移会创建表，但不会创建数据库，所以我们要提前创建好数据库
```markdown
pip install mysql-python
```
出现异常，我到PYPI查询后发现
>MySQL-3.23 through 5.5 and Python-2.4 through 2.7 are currently supported. Python-3.0 will be supported in a future release. PyPy is supported.

问题出在还不支持python3！！
我去MySQL官网查python的API
```markdown
pip install mysql-connector-python
```
安装成功

* 在mysql中创建数据库
```markdown
CREATE DATABASE test2 CHARSET utf8 COLLATE utf8_general_ci;

下面这句效果多一点，如果数据库不存在才创建
CREATE DATABASE IF NOT EXISTS test2 DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```
* 打开settings.py文件，修改DATABASES项
```markdown
# test2/setting.py

# 使用mysql数据库
DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',
        'ENGINE': 'mysql.connector.django',
        'NAME': 'test2',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '8080',  # Docker:mysql-data 默认端口3306映射到8080 
        'OPTION': {
            'autocommit': True,
        }
    }
}

```
* 生成应用booktest
```markdown
cd test2
python manage.py startapp booktest
```
生成应用`booktest`的时候出现异常

`django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module: No module named 'MySQLdb'`

由于mysql-python不支持python3，我安装的是官方的API，这里在配置setting.py时与视频是有区别的！！

官方参考文档链接[Connector/Python Django Back End](https://dev.mysql.com/doc/connector-python/en/connector-python-django-backend.html)
* 注册应用
```markdown
# test2/setting.py

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'booktest',
)
```
### 定义模型
* 关于模型的字段:

其中一般不用`FileField`,`ImageField`,因为上传容量大的二进制文件到数据库里，导致数据库容量很大，不好维护

一般做法是上传文件到服务器里，把文件路径记录下来，存到数据库，其实存储的路径就是字符串

* 关于字段约束

`null`:就是能不能将`null`存到数据库

`blank`:表单验证范畴，就是在admin添加数据的时候，该字段能不能为空，就是做这样一个验证的作用！

`default`:这个约束好像不管用

* 定义模型
```markdown
# booktest/models.py

from django.db import models

# Create your models here.


class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField(db_column='pub_date')  # 设置admin字段名为pub_date
    # 阅读量，顺便测试default有没有用
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(null=False)  # 评论量不能为空
    isDelete = models.BooleanField(default=False)

    # 定义元信息
    class Meta:
        db_table = 'bookinfo'  # 定义数据表名称,默认表名为 booktest_bookinfo


class HeroInfo(models.Model):
    hname = models.CharField(max_length=10)
    hgender = models.BooleanField(default=True)
    hcontent = models.CharField(max_length=1000)
    idDelete = models.BooleanField(default=False)
    book = models.ForeignKey(BookInfo)

```
已经注册过了，所以下一步生成迁移，执行迁移
```markdown
python manage.py makemigrations
python manage.py migrate
```

* 管理器Manager

>objects：是Manager类型的对象，用于与数据库进行交互,相当于ORM;
当定义模型类时没有指定管理器，则Django会为模型类提供一个名为objects的管理器

查询BookInfo的全部对象`BookInfo.objects.all()`

>支持明确指定模型类的管理器

```markdown
class BookInfo(models.Model):
    ...
    books = models.Manager()  # 明确指定管理器
```

当为模型类指定管理器后，django不再为模型类生成名为objects的默认管理器

* 自定义管理器
>管理器是Django的模型进行数据库的查询操作的接口，Django应用的每个模型都拥有至少一个管理器;

管理器应用1-更改默认查询集：修改管理器返回的原始查询集-重写get_queryset()方法
```markdown
# booktest/models.py

class BookInfoManager(models.Manager):
    """自定义Manager，模型类的管理器"""
    def get_queryset(self):
        """重写管理器Manager的get_querset方法，返回未逻辑删除的对象"""
        return super(BookInfoManager, self).get_queryset().filter(isDelete=False)


class BookInfo(models.Model):
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateTimeField(db_column='pub_date')  # 设置admin字段名为pub_date
    # 阅读量，顺便测试default有没有用
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(null=False)  # 评论量不能为空
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.btitle

    # 定义元信息
    class Meta:
        db_table = 'bookinfo'  # 定义数据表名称,默认表名为 booktest_bookinfo

    book1 = models.Manager()  # 指定管理器
    book2 = BookInfoManager()  # 自定义管理器
```
测试
```markdown
python manage.py shell

>>> from booktest.models import BookInfo
>>> BookInfo.book1.all()
[<BookInfo: 射雕英雄传>, <BookInfo: 天龙八部>, <BookInfo: 笑傲江湖>, <BookInfo: 雪山飞狐>]
>>> BookInfo.book2.all()
[<BookInfo: 射雕英雄传>]

```
>以往创建一个BookInfo的对象，并保存，需要写很多行代码，有没有办法可以更加快捷的创建对象吗？
1. `b = BookInfo(btitle, bpub_date)`,用`__init__`方法实现
但是会出现异常，原因是父类Model已经用了`__init__`方法了
2. 用类方法
```markdown
# booktest/models.py

# 类方法创建对象
@classmethod
def create(cls, btitle, bpub_date, bread=0, bcomment=0, isDelete=False):
    b = BookInfo()
    b.btitle = btitle
    b.bpub_date = bpub_date
    b.bread = bread
    b.bcomment = bcomment
    b.isDelete = isDelete
    return b

python manage.py shell

>>> from booktest.models import BookInfo
>>> import datetime
>>> b = BookInfo.create('abc',datetime.datetime(1990,1,1))
>>> b.save()
```

管理器应用2-创建对象(官方推荐)
```markdown
# booktest/models.py

class BookInfoManager(models.Manager):
    """自定义Manager，模型类的管理器"""
    def get_queryset(self):
        """重写管理器Manager的get_querset方法，返回未逻辑删除的对象"""
        return super(BookInfoManager, self).get_queryset().filter(isDelete=False)
    
    def create(cls, btitle, bpub_date, bread=0, bcomment=0, isDelete=False):
        """创建对象"""
        b = BookInfo()
        b.btitle = btitle
        b.bpub_date = bpub_date
        b.bread = bread
        b.bcomment = bcomment
        b.isDelete = isDelete
        return b
        
python manage.py shell

>>> from booktest.models import BookInfo
>>> import datetime
>>> b = BookInfo.book2.create('123',datetime.datetime(2017,1,1))
>>> b.save()

```
* admin管理站点
注册超级管理员
```markdown
root
root
root@163.com
```
### 查询集
两个特征：
1. **惰性执行**：创建查询集不会带来任何数据库的访问，直到调用数据时，才会访问数据库
2. 在新建的查询集中，缓存为空，首次对查询集求值时，会发生数据库查询，django会将查询的结果存在查询集的缓存中，并返回请求的结果，**接下来对查询集求值将重用缓存的结果**
>何时查询集不会被缓存：当只对查询集的**部分**进行求值时会检查缓存，但是如果这部分不在缓存中，那么接下来查询返回的记录将不会被缓存，这意味着使用索引来限制查询集将不会填充缓存，如果这部分数据已经被缓存，则直接使用缓存中的数据
```markdown
query = BookInfo.objects.all()
# 情况1
for _ in query  # 缓存全部
fot _ in query[11:20]  # 调用缓存

# 情况2 
for _ in query[0:10]  # 缓存子集
for _ in query[11:20]  # 该部分不在缓存中，不缓存这部分
```
### 自关联
* 建应用，并注册应用
```markdown
python manage.py startapp areainfo
```
* 建模型,注册模型，生成迁移，执行迁移
```markdown
# booktest/models.py

class AreaInfo(models.Model):
    atitle = models.CharField(max_length=20)
    
    # 自关联， 可以写入null，admin表单可以为空，注意'self'!!
    aparent = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        db_table = 'areas'  # 表名：areas

    def __str__(self):
        return self.atitle
```
* 管理站点
```markdown
# areainfo/admin.py

class AreaInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'atitle', 'aparent']


admin.site.register(AreaInfo, AreaInfoAdmin)
```
* 视图
```markdown
# areainfo/views.py

from .models import AreaInfo


def area(request):
    _area = AreaInfo.objects.get(pk=130100)
    return render(request, 'areainfo/area.html', {'area': _area})
```
* URLs
```markdown
# test2/urls.py

from booktest import views
from areainfo.views import area

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^area/$', area, name='area'),
]
```
* templates
```markdown
# templates/areainfo/area.html

<!DOCTYPE html>
<html>
<head>
    <title>地区</title>
</head>
<body>
<div style="background: red;">
    当前地区：{{area.atitle}}

</div>
<br>
<div style="background: blue;">
    上级地区：{{area.aparent.atitle}}

</div>
<br>
<div style="background: green;">
    下级地区：
    <ul style="list-style:none;">
        {%for a in area.areainfo_set.all%}
        <li>{{a.atitle}}</li>
        {%endfor%}
    </ul>

</div>
</body>
</html>
```

## MVT-视图views
新建项目
```markdown
django-admin startproject test3
```