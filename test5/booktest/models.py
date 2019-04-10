from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=10)
    upwd = models.CharField(max_length=40)
    idDelete = models.BooleanField(default=False)


