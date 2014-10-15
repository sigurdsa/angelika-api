from django.db import models
from patient.models import Patient


class MotivationText(models.Model):
    patient = models.ForeignKey(Patient, null=False)
    text = models.TextField(default="", blank=False)
    time_created = models.DateTimeField(null=False)
