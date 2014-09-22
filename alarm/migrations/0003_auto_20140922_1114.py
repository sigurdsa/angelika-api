# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0002_auto_20140918_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alarm',
            name='treated_text',
            field=models.TextField(default=b'', blank=True),
        ),
    ]
