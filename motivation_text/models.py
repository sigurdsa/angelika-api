from django.db import models
from patient.models import Patient
from django.utils.encoding import smart_unicode


class MotivationText(models.Model):
    patient = models.ForeignKey(Patient, null=False)
    text = models.TextField(default='', blank=False)

    time_created = models.DateTimeField(null=False, auto_now_add=True, auto_now=False)

    def __unicode__(self):
        return smart_unicode(
            ("InformationText" if self.type == 'I' else 'MotivationText')
            + " for " + self.patient.user.get_full_name()
            + " created at " + str(self.time_created)
        )

    class Meta():
        ordering = ['-id']

    TEXT_INFORMATION = 'I'
    TEXT_MOTIVATION = 'M'
    TYPES = [
        (TEXT_INFORMATION, 'InformationText'),
        (TEXT_MOTIVATION, 'MotivationText'),
    ]
    type = models.CharField(max_length=1, choices=TYPES, null=False, default='M')
