# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alarm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='alarm',
            name='is_treated',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alarm',
            name='treated_text',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
