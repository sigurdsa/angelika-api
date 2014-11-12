# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0008_auto_20141111_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='is_measurement_too_high',
            field=models.BooleanField(default=False, help_text=b'If true, the alarm was created because of a too high measurement. If false, the alarm was created because of a too low measurement.'),
            preserve_default=True,
        ),
    ]
