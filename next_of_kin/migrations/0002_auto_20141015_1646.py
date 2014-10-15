# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('next_of_kin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nextofkin',
            name='address',
            field=models.CharField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='nextofkin',
            name='phone_number',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='nextofkin',
            name='relation',
            field=models.CharField(max_length=40, null=True, blank=True),
        ),
    ]
