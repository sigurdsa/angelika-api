# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0005_auto_20141020_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='time_created',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
    ]
