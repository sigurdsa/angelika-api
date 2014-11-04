# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0002_auto_20141008_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='type',
            field=models.CharField(max_length=1, choices=[(b'A', b'Activity'), (b'O', b'O2'), (b'P', b'Pulse'), (b'T', b'Temperature')]),
        ),
    ]
