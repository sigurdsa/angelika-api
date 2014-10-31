# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0013_auto_20141020_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThresholdValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.FloatField()),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('is_upper_threshold', models.BooleanField(default=True, help_text=b'If true, the threshold value is upper, if false, the threshold value is lower')),
                ('type', models.CharField(max_length=1, choices=[(b'A', b'Activity'), (b'O', b'O2'), (b'P', b'Pulse'), (b'T', b'Temperature')])),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
            options={
                'ordering': ['time_created'],
            },
            bases=(models.Model,),
        ),
    ]
