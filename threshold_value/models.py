from django.db import models
from patient.models import Patient
from django.utils.encoding import smart_unicode


class ThresholdValue(models.Model):
    patient = models.ForeignKey(Patient, null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    time_created = models.DateTimeField(null=False, auto_now_add=True, auto_now=False)
    is_upper_threshold = models.BooleanField(
        null=False, blank=False, default=True,
        help_text="If true, the threshold value is upper, if false, the threshold value is lower"
    )

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

    def __unicode__(self):
        return smart_unicode(
            "Threshold value " + self.type + " = " + str(self.value) + " for "
            + self.patient.user.first_name + " " + self.patient.user.last_name
            + " created at " + str(self.time_created)
        )

    class Meta():
        ordering = ['time_created']
