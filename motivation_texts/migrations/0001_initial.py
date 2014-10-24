# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0010_patient_hub_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='MotivationText',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'', blank=True)),
                ('time_created', models.DateTimeField()),
                ('patient', models.ForeignKey(to='patient.Patient')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
