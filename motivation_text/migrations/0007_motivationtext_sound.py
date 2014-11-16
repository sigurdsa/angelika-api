# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motivation_text', '0006_auto_20141027_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='motivationtext',
            name='sound',
            field=models.FileField(help_text=b'Must be mp3', null=True, upload_to=b'', blank=True),
            preserve_default=True,
        ),
    ]
