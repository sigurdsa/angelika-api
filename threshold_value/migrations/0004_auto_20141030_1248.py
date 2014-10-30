# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threshold_value', '0003_auto_20141030_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='thresholdvalue',
            name='type',
            field=models.CharField(max_length=1, choices=[(b'O', b'O2'), (b'P', b'Pulse'), (b'T', b'Temperature')]),
            preserve_default=True,
        ),
    ]
