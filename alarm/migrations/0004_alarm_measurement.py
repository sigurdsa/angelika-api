# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0001_initial'),
        ('alarm', '0003_auto_20140922_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='measurement',
            field=models.ForeignKey(to='measurement.Measurement', null=True),
            preserve_default=True,
        ),
    ]
