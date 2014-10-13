# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0003_auto_20141013_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='type',
            field=models.CharField(max_length=1, choices=[(b'A', b'Activity'), (b'O', b'O2'), (b'P', b'Pulse'), (b'T', b'Temperature')]),
        ),
    ]
