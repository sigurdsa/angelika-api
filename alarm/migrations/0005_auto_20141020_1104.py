# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0004_alarm_measurement'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alarm',
            options={'ordering': ['is_treated', '-time_created']},
        ),
    ]
