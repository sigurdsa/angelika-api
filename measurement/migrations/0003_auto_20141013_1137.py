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
            field=models.IntegerField(choices=[(1, b'Activity'), (2, b'O2'), (3, b'Pulse'), (4, b'Temperature')]),
        ),
    ]
