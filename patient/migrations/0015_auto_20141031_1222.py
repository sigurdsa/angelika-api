# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patient', '0014_auto_20141030_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='hub_id',
        ),
        migrations.AddField(
            model_name='patient',
            name='hub',
            field=models.OneToOneField(related_name='hub_patient', null=True, blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
