# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('next_of_kin', '0005_auto_20141021_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextofkin',
            name='phone_number',
            field=models.CharField(max_length=16, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='nextofkin',
            name='relation',
            field=models.CharField(max_length=40, null=True),
            preserve_default=True,
        ),
    ]
