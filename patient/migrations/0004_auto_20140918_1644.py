# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0003_auto_20140918_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='email',
            field=models.CharField(max_length=80, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='first_name',
            field=models.CharField(max_length=80, blank=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='last_name',
            field=models.CharField(max_length=80, blank=True),
        ),
    ]
