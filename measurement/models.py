from django.db import models
from patient.models import Patient


class Measurement(models.Model):
    patient = models.ForeignKey(Patient)
    value = models.FloatField(default=0)
    time = models.DateTimeField(null=False)

    ACTIVITY = 1
    O2 = 2
    PULSE = 3
    TEMPERATURE = 4
    TYPES = [
        (ACTIVITY, 'Activity'),
        (O2, 'O2'),
        (PULSE, 'Pulse'),
        (TEMPERATURE, 'Temperature')
    ]
    type = models.IntegerField(choices=TYPES, null=False)

