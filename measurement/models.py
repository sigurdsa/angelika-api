from django.db import models
from patient.models import Patient
from django.utils.encoding import smart_unicode


class Measurement(models.Model):
    patient = models.ForeignKey(Patient, null=False)
    value = models.FloatField(default=0.0, null=False)
    time = models.DateTimeField(null=False)

    ACTIVITY = 'A'
    CALL_ME_REQUEST = 'C'
    O2 = 'O'
    PULSE = 'P'
    TEMPERATURE = 'T'
    TYPES = [
        (ACTIVITY, 'Activity'),
        (CALL_ME_REQUEST, 'Call me request'),
        (O2, 'O2'),
        (PULSE, 'Pulse'),
        (TEMPERATURE, 'Temperature')
    ]
    type = models.CharField(max_length=1, choices=TYPES, null=False)

    BPM = 'B'
    PERCENT = 'E'
    STEPS = 'S'
    METERS = 'M'
    KCAL = 'K'
    SECONDS = 'C'
    CELSIUS = 'D'
    NONE = ''
    UNITS = [
        (BPM, 'BPM'),
        (PERCENT, '%'),
        (STEPS, 'Steps'),
        (METERS, 'Meters'),
        (KCAL, 'KCal'),
        (SECONDS, 'Seconds'),
        (CELSIUS, 'Degrees celsius'),
        (NONE, '')
    ]
    unit = models.CharField(max_length=1, choices=UNITS, null=False, blank=True, default=NONE)

    def __unicode__(self):
        return smart_unicode(
            self.type + " = " + str(self.value) + " " + self.unit + " @ " + str(self.time)
            + " for " + self.patient.user.get_full_name()
        )

    class Meta():
        ordering = ['time']
