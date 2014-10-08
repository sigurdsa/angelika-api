# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0008_auto_20140926_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='activity_max',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='activity_min',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='o2_max',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='o2_min',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='pulse_max',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='pulse_min',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='temperature_max',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='patient',
            name='temperature_min',
            field=models.FloatField(default=0),
        ),
    ]
