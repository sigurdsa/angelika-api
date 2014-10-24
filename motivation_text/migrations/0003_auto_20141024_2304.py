# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motivation_text', '0002_auto_20141015_1552'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motivationtext',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
