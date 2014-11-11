# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0007_alarm_search_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='search_tag',
            field=models.CharField(default=b'', max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
