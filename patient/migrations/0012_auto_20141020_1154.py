# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_auto_20141015_1404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='telephone',
        ),
        migrations.AddField(
            model_name='patient',
            name='phone_number',
            field=models.CharField(max_length=14, null=True, blank=True),
            preserve_default=True,
        ),
    ]
