from django.db import models
from patient.models import Patient


class Measurement(models.Model):
    patient = models.ForeignKey(Patient, null=False)
    value = models.FloatField(default=0.0, null=False)
    time = models.DateTimeField(null=False)

    ACTIVITY = 'A'
    O2 = 'O'
    PULSE = 'P'
    TEMPERATURE = 'T'
    TYPES = [
        (ACTIVITY, 'Activity'),
        (O2, 'O2'),
        (PULSE, 'Pulse'),
        (TEMPERATURE, 'Temperature')
    ]
    type = models.CharField(max_length=1, choices=TYPES, null=False)

