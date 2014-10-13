# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0009_auto_20141008_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.TextField(default=b'')),
                ('value', models.FloatField(default=0)),
                ('time_created', models.DateTimeField()),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
