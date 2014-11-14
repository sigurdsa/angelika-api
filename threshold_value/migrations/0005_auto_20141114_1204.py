# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('threshold_value', '0004_auto_20141030_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thresholdvalue',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2014, 11, 14, 11, 4, 11, 111000, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
