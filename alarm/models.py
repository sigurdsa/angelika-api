from django.db import models
from measurement.models import Measurement


class Alarm(models.Model):

    measurement = models.ForeignKey(Measurement, null=True)
    time_created = models.DateTimeField(null=False)
    is_treated = models.BooleanField(default=False, null=False)
    treated_text = models.TextField(default="", blank=True)
