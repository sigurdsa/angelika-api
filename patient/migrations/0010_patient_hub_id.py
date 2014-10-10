# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0009_auto_20141008_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='hub_id',
            field=models.CharField(max_length=12, null=True),
            preserve_default=True,
        ),
    ]
