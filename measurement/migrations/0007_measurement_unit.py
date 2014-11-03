# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0006_auto_20141028_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='unit',
            field=models.CharField(default=b'', max_length=1, choices=[(b'B', b'BPM'), (b'E', b'%'), (b'S', b'Steps'), (b'M', b'Meters'), (b'K', b'KCal'), (b'C', b'Seconds'), (b'', b'')]),
            preserve_default=True,
        ),
    ]
