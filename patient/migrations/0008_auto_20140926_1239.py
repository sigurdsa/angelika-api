# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0007_auto_20140925_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='national_identification_number',
            field=models.CharField(default=b'', help_text=b'A number consisting of date of birth + national id, (11 digits)', max_length=11),
        ),
    ]
