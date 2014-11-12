# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0009_alarm_is_measurement_too_high'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='is_measurement_too_high',
            field=models.NullBooleanField(help_text=b'If true, the alarm was created because of a too high measurement. If false, the alarm was created because of a too low measurement. Otherwise NULL.'),
            preserve_default=True,
        ),
    ]
