# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('threshold_value', '0006_auto_20141116_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thresholdvalue',
            name='time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
