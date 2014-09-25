# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customuser', '0002_myuser_identifier'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='patient',
        ),
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
