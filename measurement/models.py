from django.db import models
from patient.models import Patient


class Measurement(models.Model):

    patient = models.ForeignKey(Patient)
    type = models.TextField(default='')
    value = models.FloatField(default=0)
    time_created = models.DateTimeField(null=False)
