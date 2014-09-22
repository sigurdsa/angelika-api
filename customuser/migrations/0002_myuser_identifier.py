# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='identifier',
            field=models.CharField(default=datetime.date(2014, 9, 18), unique=True, max_length=40),
            preserve_default=False,
        ),
    ]
