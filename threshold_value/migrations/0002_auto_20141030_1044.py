# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('threshold_value', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thresholdvalue',
            options={'ordering': ['time']},
        ),
        migrations.RenameField(
            model_name='thresholdvalue',
            old_name='time_created',
            new_name='time',
        ),
    ]
