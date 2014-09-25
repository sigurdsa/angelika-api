# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_auto_20140925_1138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='normal_activity',
            new_name='activity_max',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='normal_o2',
            new_name='activity_min',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='normal_pulse_max',
            new_name='o2_max',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='normal_pulse_min',
            new_name='o2_min',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='normal_temperature_max',
            new_name='pulse_max',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='normal_temperature_min',
            new_name='pulse_min',
        ),
        migrations.AddField(
            model_name='patient',
            name='activity_access',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='o2_access',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='pulse_access',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='temperature_access',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='temperature_max',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='patient',
            name='temperature_min',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
