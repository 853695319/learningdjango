from django.db import models


class AreaInfo(models.Model):
    atitle = models.CharField(max_length=20)

    # 自关联， 可以写入null，admin表单可以为空
    aparent = models.ForeignKey('self', null=True, blank=True)

    class Meta:
        db_table = 'areas'  # 表名：areas

    def __str__(self):
        return self.atitle
