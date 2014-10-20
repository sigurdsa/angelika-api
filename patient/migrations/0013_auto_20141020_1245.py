# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0012_auto_20141020_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='city',
            field=models.CharField(max_length=120, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='zip_code',
            field=models.CharField(max_length=4, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
