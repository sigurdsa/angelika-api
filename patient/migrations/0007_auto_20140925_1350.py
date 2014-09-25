# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_auto_20140925_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='date_of_birth',
        ),
        migrations.AddField(
            model_name='patient',
            name='national_identification_number',
            field=models.CharField(default=b'', help_text=b'A number consisting of date of birth + national id, called fodselsnummer, needs to be 11 digits long', max_length=11),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='patient',
            name='activity_access',
            field=models.BooleanField(default=False, help_text=b'If True, the patient has access to view activity data in patient interface'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='o2_access',
            field=models.BooleanField(default=False, help_text=b'If True, the patient has access to view o2 data in patient interface'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='pulse_access',
            field=models.BooleanField(default=False, help_text=b'If True, the patient has access to view pulse data in patient interface'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='temperature_access',
            field=models.BooleanField(default=False, help_text=b'If True, the patient has access to view temperature data in patient interface'),
        ),
    ]
