# learningdjango
记录学习django的过程资料

django_py3.6 python3.6虚拟环境
test1 是django项目文件夹





## 创建基于Docker的Mysql
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
```
docker run -p 8080:3306 --name mysql-data -v /home/chenzhixiong/09-django/learningdjango/myconfig:/etc/mysql/mysql.conf.d -v /home/chenzhixiong/09-django/learningdjango/mysqldata:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=root -it mysql:5.7
```
意外发现，被docker挂载后的文件夹会被docker改变权限，只有docker用得了，我要用 chmod a+rwx -R * 修改权限才能使用
所以以后docker挂载的目录应设置号具体地方，不要和本地数据库共用同一目录





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
