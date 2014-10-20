from django.db import models
from measurement.models import Measurement
from django.utils.encoding import smart_unicode


class Alarm(models.Model):

    measurement = models.ForeignKey(Measurement, null=True)
    time_created = models.DateTimeField(null=False)
    is_treated = models.BooleanField(default=False, null=False)
    treated_text = models.TextField(default="", blank=True)

    class Meta():
        ordering = ['is_treated', '-time_created']

    def __unicode__(self):
        s = "Alarm at " + str(self.time_created)
        if self.measurement:
            s += " for " + self.measurement.patient.user.get_full_name()
        return smart_unicode(s)
