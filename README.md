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

>如果定义了__unicode__()方法但是没有定义__str__()方法，Django会自动提供一个__str__()方法调用__unicode__()方法，然后把结果转换为UTF-8编码的字符串对象。在实际开发中，建议：只定义__unicode__()方法，需要的话让Django来处理字符串对象的转换。
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
写在前面的话：

如果后续发现要该模型类，后续改了时迁移不过去的，会报错

解决办法，改模型类，生成迁移，但不执行迁移，自己手动到数据库改表结构


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

bug:
[AttributeError: 'decimal.Decimal' object has no attribute 'decode'](https://stackoverflow.com/questions/52789427/attributeerror-decimal-decimal-object-has-no-attribute-decode)

问题：出在`mysql-connector-python`版本太高
解决：
```text
pip install mysql-connector-python==8.0.5

Versions as new as 8.0.12 seem to work, failing after 8.0.13
```


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
新建app
```markdown
python manage.py startapp booktest
```
### 配置URLconf
```markdown
# test3/urls.py

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^booktest/', include('booktest.urls'))
]


# booktest/urls.py

from django.conf.urls import url
from . import views

urlpatterns = {
    url(r'^$', views.index, name='index')
}


# booktest/views.py

from django.http import HttpResponse


def index(request):
    return HttpResponse("hello world")

# 测试
python manage.py runserver
http://127.0.0.1:8000/booktest/

```
### URL的反向解析-重定向

如果在视图、模板中使用硬编码的链接，在urlconf发生改变时，维护是一件非常麻烦的事情

解决：在做链接时，通过指向urlconf的名称，动态生成链接地址

视图：使用django.core.urlresolvers.reverse()函数

模板：使用url模板标签

举个例子：

在index.html模板中，超链接是硬编码的，此时的请求地址为“127.0.0.1/1/”

`<a href="{{book.id}}">`

看如下情况：将urlconf中详细页改为如下，链接就找不到了

`url(r'^book/([0-9]+)/$', views.detail),`

原地址：127.0.0.1/1/

此时的请求地址应该为“127.0.0.1/book/1/”

问题总结：如果在模板中地址硬编码，将来urlconf修改后，地址将失效

解决：使用命名的url设置超链接

修改test1/urls.py文件，**在include中设置namespace**

`url(r'^admin/', include(admin.site.urls, namespace='booktest')),`

修改booktest/urls.py文件，**设置name**

`url(r'^book/([0-9]+)/$', views.detail, name="detail"),`

修改index.html模板中的链接

`<a href="{%url 'booktest:detail' book.id%}">`

### 404视图
>如果在settings中DEBUG设置为True，那么将永远不会调用404视图，而是显示URLconf 并带有一些调试信息
```markdown
# test3/setting.py

DEBUG = False
ALLOWED_HOSTS = ['*']  # 谁都可以请求该主机
```

### Request对象
>GET：一个类似于字典的对象，包含get请求方式的所有参数
>
>POST：一个类似于字典的对象，包含post请求方式的所有参数

>类似于字典的对象:QueryDict对象
>
>与python字典不同，QueryDict类型的对象用来处理同一个键带有多个值的情况

* 关于URL

```markdown
www.itcast.cn/ 
├── b.html <a href="/b.html"></a> 多了斜杠'/'表示到根目录找 b.html
└── c
    └── a.html <a href="www.itcast.cn/c/a.html">当前页</a>
    └── b.html <a href="b.html"></a> 在当前目录下找 b.html

```
* POST测试时遇到 403
>Forbidden (403)
>
>CSRF verification failed. Request aborted.

解决办法：
注释`setting.py`中 MIDDLEWARE_CLASSES的'django.middleware.csrf.CsrfViewMiddleware',

* session 测试遇到OperationalError

>OperationalError at /booktest/sessionTest2_handle/
>
>no such table: django_session

原因是，数据库没有相应的表结构，为什么没有相应的表结构，是因为我们没有执行过**迁移**

解决：改sqllite为之前用过的mysql数据库，这里有表结构，因为之前项目执行过迁移

表名：django_session

django_session.session_data base64加密的，特征是最后有1个或2个等号，可以解开来看看
```markdown
In [30]: import base64

In [31]: s = 'ZmE1MGY5MzljMTA4NjgzZjRmNzIwNTg5ZDA3NWQ5MDcyNjI0MzhjOTp7InVzZXJuYW
    ...: 1lIjoicHl0aG9uIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ=='

In [32]: result = base64.b64decode(s)

In [33]: result
Out[33]: b'fa50f939c108683f4f720589d075d907262438c9:{"username":"python","_session_expiry":0}'
```
* 使用Redis缓存session
```markdown
pip install django-redis-sessions

# test3/setting.py

# 使用Redis缓存session
SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': '',
    'prefix': 'session',
    'socket_timeout': 1
}

# 启动redis
redis-server /etc/redis.conf
# 确认是否启动
ps -ajx | grep redis
 1733  42083  42083  42083 ?            -1 Ssl   1000   0:00 redis-server 127.0.0.1:6379

# 启动客户端
redis-cli

chenzhixiong@ubuntu:~$ redis-cli
127.0.0.1:6379> KEYS *
1) "hehe"
2) "456"
3) "123"
4) "dig"
5) "test"
6) "kuku"
7) "name"
8) "789"
9) "lalala"

# 启用session登录后
127.0.0.1:6379> KEYS *
 1) "hehe"
 2) "456"
 3) "123"
 4) "session:0lsjbiks4dzc05topkmlivvg3feqm4qs"
 5) "dig"
 6) "test"
 7) "kuku"
 8) "name"
 9) "789"
10) "lalala"

# 取session
127.0.0.1:6379> GET "session:0lsjbiks4dzc05topkmlivvg3feqm4qs"
"ZmE1MGY5MzljMTA4NjgzZjRmNzIwNTg5ZDA3NWQ5MDcyNjI0MzhjOTp7InVzZXJuYW1lIjoicHl0aG9uIiwiX3Nlc3Npb25fZXhwaXJ5IjowfQ=="

# base64解码
In [37]: s = "ZDgwNjc3YTRiODBlMWQ4MmM1MTZlZGNlZGViNDFmYzg3YjVmMWExZTp7Il9zZXNzaW9uX2V4cGlyeSI6MC
    ...: widXNlcm5hbWUiOiJzZXNzaW9uIGluIHJlZGlzIn0="
    ...: 

In [38]: result = base64.b64decode(s)

In [39]: result
Out[39]: b'd80677a4b80e1d82c516edcedeb41fc87b5f1a1e:{"_session_expiry":0,"username":"session in redis"}'


```






## MVT-模板Templates
**写模板语言时，不要随便加空格！！**

创建项目,配置数据库，模板URLs
```markdown
django-admin startproject test4
python manage.py startapp booktest
```
###变量

语法：`{{ variable }}`

当模版引擎遇到一个变量，将计算这个变量，然后将结果输出

变量名必须由字母、数字、下划线（不能以下划线开头）和点组成

当模版引擎遇到点(".") eg:{{ book.id }}，会按照下列顺序查询：

* 字典查询，例如：book['id'] ,所以不能带有括号，有括号就报错！

* 属性或方法查询，例如：book.id

* 数字索引查询，例如：book[id] 列表或元组

如果变量不存在， 模版系统将插入'' (空字符串)

在模板中调用方法时不能传递参数，因为不能写括号

### django 加减乘除，求余
```markdown
django模板只提供了加法的filter，没有提供专门的乘法和除法运算；
django提供了widthratio的tag用来计算比率，可以变相用于乘法和除法的计算。
加法
{{value|add:10}}
note:value=5,则结果返回15

减法
{{value|add:-10}}
note:value=5,则结果返回-5，加一个负数就是减法了

乘法
{% widthratio 5 1 100%}
note:等同于：(5 / 1) * 100 ，结果返回500，withratio需要三个参数，它会使用参数1/参数2*参数3的方式进行运算，进行乘法运算，使「参数2」=1

除法
{% widthratio 5 100 1%}
note:等同于：(5 / 100) * 1,则结果返回0.05,和乘法一样，使「参数3」= 1就是除法了。

求余 
{% if forloop.counter|divisibleby:"4" %}
整出4的数
{% if forloop.counter|divisibleby:"2" %} --> 整除2的数
```

### URL反向解析
一般正则在在`$`前加斜杠`/`，不在`^`后加`/`,eg: `r"^admin/$"`
1. 硬编码链接
```markdown
# test4/urls.py

url(r'^', include('booktest.urls', namespace='booktest')),

# booktest/view.py

def show(request, id):
    context = {'id':id}
    return render(request, 'booktest/show.html', context)

# booktest/urls.py

url(r'^(\d+)/$', views.show, name='show'),
# http://127.0.0.1:8000/1233445667/

# booktest/index.html

<div>
    <h4>URL反向解析</h4>
    <a href="11/">显示id</a>
</div>

# booktest/show.html

<div>
    id: {{ id }}
</div>

```

2.URL反向解析

>正常：根据`booktest/123`-->URL
>
>反向：根据URL --> `booktest/123`
```markdown
# test4/urls.py

url(r'^booktest/', include('booktest.urls', namespace='booktest')),

# booktest/index.html

{% url 'booktest:show' '123' as show_url %}
<a href="{{ show_url}}">显示id</a>
```

>异常：django 报错’ set’ object is not reversible
原因是
```markdown
# test4/urls.py

urlpatterns = {}  # 这里写错了！ 不应该是 set类型
urlpatterns = []  # 这样才对！！

```
3.原理详解：反查带命名空间的URL

当解析一个带命名空间的URL（例如'polls:index'）时，Django 将切分名称为多个部分，然后按下面的步骤查找：

* 首先，Django 查找匹配的**应用命名空间**(在这个例子中为'polls'）。这将得到该**应用实例的一个列表**。
如果有一个当前应用被定义，Django 将查找并返回那个实例的URL 解析器。当前应用可以通过请求上的一个属性指定。预期会具有多个部署的应用应该设置正在处理的request 的current_app 属性。

>Changed in Django 1.8: 
>
>在以前版本的Django 中，你必须在用于渲染模板的每个Context 或 RequestContext上设置current_app 属性。

* 当前应用还可以通过reverse() 函数的一个参数手工设定。
* 如果没有当前应用。Django 将查找一个默认的应用实例。默认的应用实例是实例命名空间 与应用命名空间 一致的那个实例（在这个例子中，polls 的一个叫做'polls' 的实例）。
* **如果没有默认的应用实例，Django 将挑选该应用最后部署的实例，不管实例的名称是什么。**
* 如果提供的命名空间与第1步中的应用命名空间 不匹配，Django 将尝试直接将此命名空间作为一个实例命名空间查找。
* 如果有嵌套的命名空间，将为命名空间的每个部分重复调用这些步骤直至剩下视图的名称还未解析。然后该视图的名称将被解析到找到的这个命名空间中的一个URL。
例子¶

为了演示解析的策略，考虑教程中polls 应用的两个实例：'author-polls' 和'publisher-polls'。假设我们已经增强了该应用，在创建和显示投票时考虑了实例命名空间。
```
# urls.py
from django.conf.urls import include, url

urlpatterns = [
    url(r'^author-polls/', include('polls.urls', namespace='author-polls', app_name='polls')),
    url(r'^publisher-polls/', include('polls.urls', namespace='publisher-polls', app_name='polls')),
]

# polls/urls.py
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    ...
]
```
根据以上设置，可以使用下面的查询：

如果其中一个实例是当前实例 —— 如果我们正在渲染'author-polls' 实例的detail 页面 —— 'polls:index' 将解析成'author-polls' 实例的主页面；例如下面两个都将解析成"/author-polls/"。

在基于类的视图的方法中：

reverse('polls:index', current_app=self.request.resolver_match.namespace)

和在模板中：

{% url 'polls:index' %}

注意，在模板中的反查需要添加request 的current_app 属性，像这样：
```
def render_to_response(self, context, **response_kwargs):
    self.request.current_app = self.request.resolver_match.namespace
    return super(DetailView, self).render_to_response(context, **response_kwargs)
```
如果没有当前实例 —— 如果我们在站点的其它地方渲染一个页面 —— 'polls:index' 将解析到最后注册的polls的一个实例。因为没有默认的实例（命名空间为'polls'的实例），将使用注册的polls 的最后一个实例。它将是'publisher-polls'，因为它是在urlpatterns中最后一个声明的。

>**'author-polls:index' 将永远解析到 'author-polls' 实例的主页（'publisher-polls' 类似）。**
>
> 所以用实例命名空间更准确

如果还有一个默认的实例 —— 例如，一个名为'polls' 的实例 —— 上面例子中唯一的变化是当没有当前实例的情况（上述第二种情况）。在这种情况下 'polls:index' 将解析到默认实例而不是urlpatterns 中最后声明的实例的主页。

### html 转义

>html.escape(s, quote=True)
>
>将字符串 s 中的字符``&`` 、 < 和 > 转换为安全的HTML序列。 如果需要在 HTML 中显示可能包含此类字符的文本，请使用此选项。 如果可选的标志 quote 为真值，则字符 (") 和 (') 也被转换；这有助于包含在由引号分隔的 HTML 属性中，如 <a href="...">。
>
>3.2 新版功能.
>
>html.unescape(s)
>
>将字符串 s 中的所有命名和数字字符引用 (例如 &gt;, &#62;, &#x3e;) 转换为相应的Unicode字符。 此函数使用HTML 5标准为有效和无效字符引用定义的规则，以及 HTML 5 命名字符引用列表。

默认情况下，Django 中的每个模板会自动转义每个变量的输出。
{{ var }} 会被转义，但是用HttpResponse方法输出带标签的就不会被转义
明确地说，下面五个字符被转义：

    < 会转换为&lt;
    > 会转换为&gt;
    '（单引号）转换为&#39;
    " (双引号)会转换为 &quot;
    & 会转换为 &amp;


* python3 实现转义和反转义
```
In [78]: import html

In [79]: s='<b>default</b>'

In [80]: result = html.escape(s)

In [81]: print(result)
&lt;b&gt;default&lt;/b&gt;

In [82]: s = html.unescape(result)

In [83]: print(s)
<b>default</b>
```

* django 默认开启转义,是出于安全考虑，防止传入代码直接执行
```markdown
> 转义 &gt;

s = '<h1>123</h1>'
{{ s|escape }} -> &lt;h1&gt;123&lt;/h1&gt;
```
* 关闭转义
```markdown
s = '<h1>123</h1>'
{{ s|safe }} -> 123
```
* 字面值默认不转义
像我们之前提到的那样，过滤器参数可以是字符串：
```markdown
{{ data|default:"This is a string literal." }}
```
所有字面值字符串在插入模板时都 不会带有任何自动转义 -- 它们的行为类似于通过 safe过滤器传递。 背后的原因是，模板作者可以控制字符串字面值的内容，所以它们可以确保在模板编写时文本经过正确转义。

也即是说你应该这样编写
```markdown
{{ data|default:"3 &lt; 2" }}
```

…而不是：
```markdown
{{ data|default:"3 < 2" }}  {# Bad! Don't do this. #}
```

这不会影响来源于变量自身的数据。 变量的内容在必要时仍然会自动转义，因为它们不受模板作者的控制。

* 总结

从视图传入模板的数据默认转义，直接在HTML定义的数据不自动转义

### CSRF
只有POST请求时，才关系到CSRF
```markdown
# booktest/views.py

# csrf
def csrf1(request):
    return render(request, 'booktest/csrf1.html')


def csrf2(request):
    uname = request.POST['uname']
    return HttpResponse(uname)

配置booktest/urls.py



# 用本地IP地址开启服务
python manage.py runserver 192.168.0.107:8000

# 换一台机器访问
192.168.0.107：8000/csrf1/
提交出现Forbidden

# 到setting.py注释csrf

MIDDLEWARE_CLASSES = (
    # 'django.middleware.csrf.CsrfViewMiddleware',
)

# 重启服务，再次提交，成功
在另一台电脑把网页源代码复制下来，设置好<form>的表单提交地址，就可以本地提交信息成功！
这样别有用心的人就很容易搞你的网站了

# 所以不能注释setting的csrf
# 但问题是，我自己用本地IP地址也无法访问阿
# 解决方法：加 csrf保护标签

<form action="{% url 'booktest:csrf2' %}" method="post">
    {% csrf_token %}
    <input type="text" name="uname">
    <input type="submit" value="提交">
</form>

```
### 验证码
`{% csrf_token %}`实际还不够强，人家把网页复制过去还是能用

为了防止暴力请求，用验证码
* 安装Pillow

[Pillow](https://pillow.readthedocs.io/en/latest/index.html)


## Django-高级
### 静态文件
STATIC_URL的作用，可以隐藏实际文件路径
```
# setting.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    # 注意写法！！ 不是 /static/ 
    os.path.join(BASE_DIR, 'static'),
]

# index.html
<img src="/static/booktest/test.jpg" alt="图片" style="width: 100%;">
根据src可以看出图片文件加载路径
```
更改STATIC_URL,还能找到图片吗？
```
# setting.py
STATIC_URL = '/abc/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# index.html
<img src="/abc/booktest/test.jpg" alt="图片" style="width: 100%;">
```
硬编码地址匹配规则：
* 先匹配逻辑路径 STATIC_URL
* 在匹配物理地址 STATICFILES_DIRS

动态解析：static模板标签动态解析URL

### 第三方富文本编辑器
#### django-tinymce

我到pypi检索后发现，不支持py3.6，最高支持到py3.5,我尝试使用，但出现异常

    TypeError at /admin/mytinymce/mymodel/add/

    build_attrs() takes from 1 to 2 positional arguments but 3 were given

#### django-ckeditor

到网上找到另一个比较知名的第三方富文本编辑器

其中有一个要点，管理`ckeditor`的相关静态文件
到`/django_py3.6/lib/python3.6/site-packages/ckeditor/static/ckeditor`把静态文件复制到项目文件夹`static/ckeitor`

admin后端
```
# 安装

pip install django-ckeditor

# setting.py

Add ckeditor to your INSTALLED_APPS setting

# myapp/models.py

from django.db import models
from ckeditor.fields import RichTextField


class Post(models.Model):
    content = RichTextField()

# myapp/admin.py

from django.contrib import admin
from .models import *


admin.site.register(Post)

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

it work!
```

前端
```text
<form>
    {{ myform.media }}
    {{ myform.as_p }}
    <input type="submit"/>
</form>

or

or you can load the media manually as it is done in the demo app:

{% load static %}
<script type="text/javascript" src="{% static "ckeditor/ckeditor-init.js" %}"></script>
<script type="text/javascript" src="{% static "ckeditor/ckeditor/ckeditor.js" %}"></script>


```



### 全文搜索
#### 异常1

* 我按教程走到  **9.生成索引** 的步骤时出现异常
>django.core.exceptions.ImproperlyConfigured: Passing a 3-tuple to include() is not supported. Pass a 2-tuple containing the list of patterns and app_name, and provide the namespace argument to include() instead.

起初我就很纳闷 `urls.py` 的设置应该时没有异常的，但是却说我传递了过多的参数

我重开一个项目 test7 重新按 ``django-haystack`` 官方文档走一遍时，在我配置 `urls.py` 时发现异常点

```text

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/2.2/topics/http/urls/

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^search/', include('haystack.urls')),
]
```
我的django莫名其妙地升级到 `django 2.2` , 当我重新安装 `pip install django==1.11` 时，发现我安装的
`django-hatstack 2.8.1` 需要 `django 2.2`时，我就知道问题处在 `django` 的版本上了

* 解决办法：

去 `django-haystakc` Github 网页上查询 `changelog` 版本变更记录，决定使用 `v2.7.0`

test7 superuser: root qew96898

#### 全文检索效果对比
* with jieba

在test6，用对版本后根据教程就能走下去了

异常二：有些结果搜索不到，因为中文分词的词库不好

尝试一些一定有的词语，如：中国，美国，英国就可以

这个中文分词用着很一般，我输入 “国” ，都不能搜索到 中国，美国，英国

好像全文检索一定要输入一个完整的词，比如 hello world，用hello，world可以搜索到，但是用单个字母就没反应

* without jieba

在test7，我没有安jango-haystack+jieba装`jieba`,也可以搜索中文，但是结果更加糟糕，好像只能匹配开头的‘中国’

### celery
* 本地环境
```text
pytho 3.6
django==1.11
```
* 搭建开发环境
```text
# 对 Redis 的支持需要额外的依赖。你可以用 celery[redis] 捆绑 同时安装 Celery 和这些依赖：

pip install -U celery[redis]

# reids（与python接口API） 版本过高将导致 AttributeError: 'str' object has no attribute 'items' django

pip install redis==2.10.6

# django-celery 库基于 Django ORM和缓存框架实现了结果存储后端

pip install django-celery==3.2.2 
```
* 建项目
```text
django-admin startproject myproject
cd myproject
python manage.py startapp demoapp
```

* Celery 配置
```text
# setting.py

INSTALLED_APPS += [
    'kombu.transport.django',
    'demoapp',
    'djcelery',
]
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

# celery settings
# celery中间人 redis://redis服务所在的ip地址:端口/数据库号
BROKER_URL = 'redis://localhost:6379/3'

# celery内容等消息的格式设置
CELERY_ACCEPT_CONTENT = ['application/json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# celery时区设置，使用settings中TIME_ZONE同样的时区
CELERY_TIMEZONE = TIME_ZONE

import djcelery
djcelery.setup_loader()
# celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'redis://localhost:6379/3'
```
>开头增加如上配置文件，根据实际情况配置redis的地址和端口，时区一定要设置为Asia/Shanghai。否则时间不准确回影响定时任务的运行。
>
>上面代码首先导出djcelery模块，并调用setup_loader方法加载有关配置；注意配置时区，不然默认使用UTC时间会比东八区慢8个小时。其中INSTALLED_APPS末尾添加两项，分别表示添加celery服务和自己定义的apps服务。

* 定义celery实例
```text
# 与 manage.py 同级目录建立 celery.py

from __future__ import absolute_import, unicode_literals

from celery import Celery
from django.conf import settings
import os

# 获取当前文件夹名，即为该Django的项目名
project_name = os.path.split(os.path.abspath('.'))[-1]
project_settings = '%s.settings' % project_name

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)

# 实例化Celery
app = Celery(project_name)

# 使用django的settings文件配置celery
app.config_from_object('django.conf:settings')

# Celery加载所有注册的应用
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
```
>接着，需要在 myproject/myproject/__init__.py 模块中导入这个 Celery 实例（也就是 app）。这样可以确保当 Django 启动时可以加载这个 app，并且 @shared_task 装饰器（后面会提到）也能使用这个 app.
```text
# myproject/myproject/__init__.py

from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app # noqa
```
>使用 @shared_task 装饰器
你很可能在可重用的 Django APP 中编写了一些任务，但是 Django APP 不能依赖于具体的 Django 项目，所以你无法直接导入 Celery 实例。
@shared_task 装饰器能让你在没有具体的 Celery 实例时创建任务：
* task
myproject/demoapp/task.py

```text
from __future__ import absolute_import
from celery import shared_task
import time


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def time_consuming_fun():
    for i in range(5):
        time.sleep(1)
        print(i)
    return 'ok'
```
* 视图
myproject/demoapp/views.py
```text
from django.shortcuts import render
from django.http import JsonResponse
from .task import *


def celery_test(request):
    # 异步调用
    time_consuming_fun.delay()
    # 直接调用
    # time_consuming_fun()
    return JsonResponse({'msg': 'ok', 'code': 200})
```
* urls
```text
myproject/myproject/urls.py

url(r'^', include('demoapp.urls')),

myproject/demoapp/urls.py

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^celerytest/$', views.celery_test),
]
```
* 迁移
```text
python manage.py makemigrations
python manage.py migrate
```
* 超级管理员
```text
python manage.py createsuperuser

root qew96898
```
* 启动django-web
```text
python manage.py runserver
```
* 启动celery

在项目根目录下，即managy同级文件目录下，输入命令：
```text

 celery -A myproject worker -l info
```
此时celery在终端窗口运行，关闭终端celery就会停止。

输入命令
```
celery multi start w1 -A myproject -l info --logfile = celerylog.log --pidfile = celerypid.pid
```
此时celery为守护进程，日志记录在celerylog.log里。

日志文件可以指定路径PATH/celerylog.log，此时会在指定路径下创建日志文件。进程号文件类似。

停止或重启将start换为stop或restart即可。

所以需记录w1，即需记录woker的名称来方便重启和停止。


# 天天生鲜
## 注册
账户密码1111111111 10个1
