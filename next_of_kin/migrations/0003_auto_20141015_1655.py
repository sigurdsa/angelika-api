# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('next_of_kin', '0002_auto_20141015_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextofkin',
            name='first_name',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='nextofkin',
            name='last_name',
            field=models.CharField(max_length=80),
        ),
    ]
