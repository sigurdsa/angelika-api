# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0011_auto_20141015_1404'),
    ]

    operations = [
        migrations.CreateModel(
            name='NextOfKin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=80, null=True)),
                ('last_name', models.CharField(max_length=80, null=True)),
                ('address', models.CharField(max_length=250)),
                ('phone_number', models.CharField(max_length=16, null=True)),
                ('priority', models.IntegerField(default=0)),
                ('relation', models.CharField(max_length=40, null=True)),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
