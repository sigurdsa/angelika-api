from django.db import models
from patient.models import Patient
from django.utils.encoding import smart_unicode

class MotivationText(models.Model):
    patient = models.ForeignKey(Patient, null=False)
    text = models.TextField(default='', blank=False)
    time_created = models.DateTimeField(null=False, auto_now_add=True, auto_now=False)


    def __unicode__(self):
        return smart_unicode(
            "Motivational text for " + self.patient.user.first_name + " " + self.patient.user.last_name
            + " created at " + str(self.time_created)
        )

    class Meta():
        ordering = ['-id']
