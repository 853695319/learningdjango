# learningdjango
记录学习django的过程资料

django_py3.6 python3.6虚拟环境
test1 是django项目文件夹
## 创建基于Docker的Mysql
```
docker run --name mysql-data \
           -p 8080:3306 \
           -v /home/chenzhixiong/09-django/learningdjango/mysqldata/myconfig:/etc/mysql/mysql.conf.d \
           -v /var/lib/mysql:/var/lib/mysql \
           -e MYSQL_ROOT_PASSWORD="root" \
           -d mysql:5.7 \
           --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```
### 问题1：
ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)

### 问题2：
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

## Django-建立应用booktest 模型models 测试
在test1项目文件夹下创建booktest模块
```
python manage.py startapp booktest
```
在 models.py 定义模型类
定义为模型类后可以到 test1项目文件夹下 测试下
```
python manage.py runserver 8080
```
但实际并没有用到你刚刚做到，你需要先进行 迁移 应用
把应用注册到 /test1/test1/settings.py INSTALLED_APPS

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
在 settings.py 
```markdown
LANGUSGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
```
* 向admin注册booktest的模型
test1/booktest/admin.py
```
from django.contrib import admin
# python3 包的相对导入
from .models import BookInfo, HeroInfo
admin.site.register(BookInfo)
admin.site.register(HeroInfo)
```
* 修改后台管理admin网页
```markdown
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

```