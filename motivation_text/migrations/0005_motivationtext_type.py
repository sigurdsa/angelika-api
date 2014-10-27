# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motivation_text', '0004_auto_20141027_1124'),
    ]

    operations = [
        migrations.AddField(
            model_name='motivationtext',
            name='type',
            field=models.CharField(default=b'M', max_length=1, choices=[((b'I',), b'InformationText'), (b'M', b'MotivationText')]),
            preserve_default=True,
        ),
    ]
