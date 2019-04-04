# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bookinfo',
            old_name='bpub',
            new_name='bpub_date',
        ),
    ]
