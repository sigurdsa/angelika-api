# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('next_of_kin', '0004_auto_20141017_1222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nextofkin',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='nextofkin',
            name='last_name',
        ),
        migrations.AddField(
            model_name='nextofkin',
            name='full_name',
            field=models.CharField(default='', max_length=160),
            preserve_default=False,
        ),
    ]
