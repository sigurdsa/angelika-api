# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0016_auto_20141106_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='show_activity',
            field=models.BooleanField(default=True, help_text=b'If True, activity data is shown in the interface for health professionals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='show_o2',
            field=models.BooleanField(default=True, help_text=b'If True, O2 data is shown in the interface for health professionals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='show_pulse',
            field=models.BooleanField(default=True, help_text=b'If True, heart rate data is shown in the interface for health professionals'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='show_temperature',
            field=models.BooleanField(default=True, help_text=b'If True, temperature data is shown in the interface for health professionals'),
            preserve_default=True,
        ),
    ]
