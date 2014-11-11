# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0006_auto_20141104_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='search_tag',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
