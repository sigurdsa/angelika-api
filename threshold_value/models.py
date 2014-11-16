from django.db import models
from patient.models import Patient
from django.utils.encoding import smart_unicode
from django.utils import timezone


class ThresholdValue(models.Model):
    patient = models.ForeignKey(Patient, null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    time = models.DateTimeField(null=False, default=timezone.now)
    is_upper_threshold = models.BooleanField(
        null=False, blank=False, default=False,
        help_text="If true, the threshold value is upper, if false, the threshold value is lower"
    )

    O2 = 'O'
    PULSE = 'P'
    TEMPERATURE = 'T'
    TYPES = [
        (O2, 'O2'),
        (PULSE, 'Pulse'),
        (TEMPERATURE, 'Temperature')
    ]
    type = models.CharField(max_length=1, choices=TYPES, null=False)

    def __unicode__(self):
        return smart_unicode(
            ('Upper' if self.is_upper_threshold else 'Lower') + " threshold value "
            + self.type + " = " + str(self.value)
            + " for " + self.patient.user.first_name + " " + self.patient.user.last_name
            + " starting " + str(self.time)
        )

    class Meta():
        ordering = ['time']
