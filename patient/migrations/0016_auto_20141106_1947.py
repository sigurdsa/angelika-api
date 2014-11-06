# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0015_auto_20141031_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='national_identification_number',
            field=models.CharField(default=b'', help_text=b'A number consisting of date of birth + national id, (11 digits)', unique=True, max_length=11),
            preserve_default=True,
        ),
    ]
