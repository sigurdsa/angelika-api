# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('threshold_value', '0005_auto_20141114_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thresholdvalue',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 15, 23, 46, 40, 415000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
