# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('next_of_kin', '0003_auto_20141015_1655'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nextofkin',
            options={'ordering': ['priority']},
        ),
    ]
