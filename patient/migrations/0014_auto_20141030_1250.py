# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0013_auto_20141020_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='o2_max',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='o2_min',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='pulse_max',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='pulse_min',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='temperature_max',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='temperature_min',
        ),
    ]
