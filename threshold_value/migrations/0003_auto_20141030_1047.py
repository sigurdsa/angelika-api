# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threshold_value', '0002_auto_20141030_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thresholdvalue',
            name='is_upper_threshold',
            field=models.BooleanField(default=False, help_text=b'If true, the threshold value is upper, if false, the threshold value is lower'),
            preserve_default=True,
        ),
    ]
