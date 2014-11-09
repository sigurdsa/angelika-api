# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0007_measurement_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='unit',
            field=models.CharField(default=b'', max_length=1, blank=True, choices=[(b'B', b'BPM'), (b'E', b'%'), (b'S', b'Steps'), (b'M', b'Meters'), (b'K', b'KCal'), (b'C', b'Seconds'), (b'D', b'Degrees celsius'), (b'', b'')]),
            preserve_default=True,
        ),
    ]
