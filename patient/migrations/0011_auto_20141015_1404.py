# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_patient_hub_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='activity_max',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='activity_min',
        ),
    ]
