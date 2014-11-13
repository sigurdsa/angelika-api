# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0011_auto_20141112_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='measurement',
            field=models.OneToOneField(null=True, to='measurement.Measurement'),
            preserve_default=True,
        ),
    ]
