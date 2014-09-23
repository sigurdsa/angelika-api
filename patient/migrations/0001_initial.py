# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.TextField(default=b'')),
                ('first_name', models.TextField(default=b'')),
                ('last_name', models.TextField(default=b'')),
                ('date_of_birth', models.DateField()),
                ('telephone', models.IntegerField(default=None)),
                ('normal_pulse_max', models.IntegerField(default=0)),
                ('normal_pulse_min', models.IntegerField(default=0)),
                ('normal_o2', models.IntegerField(default=0)),
                ('normal_temperature_max', models.IntegerField(default=0)),
                ('normal_temperature_min', models.IntegerField(default=0)),
                ('normal_activity', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
