# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('motivation_text', '0003_auto_20141024_2304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='motivationtext',
            options={'ordering': ['-id']},
        ),
    ]
