# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motivation_text', '0005_motivationtext_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='motivationtext',
            name='type',
            field=models.CharField(default=b'M', max_length=1, choices=[(b'I', b'InformationText'), (b'M', b'MotivationText')]),
        ),
    ]
