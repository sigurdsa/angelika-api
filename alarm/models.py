from django.db import models
from measurement.models import Measurement
from django.utils.encoding import smart_unicode


class Alarm(models.Model):
    measurement = models.OneToOneField(Measurement, null=True)
    time_created = models.DateTimeField(null=False, auto_now_add=True, auto_now=False)
    is_treated = models.BooleanField(default=False, null=False)
    treated_text = models.TextField(default="", blank=True)
    search_tag = models.CharField(default="", blank=True, max_length=50)
    reason = models.NullBooleanField(
        null=True, blank=True, default=None,
        help_text="If true, the alarm was created because of a too high measurement. If false, the alarm was"
                  " created because of a too low measurement. Otherwise NULL."
    )

    class Meta():
        ordering = ['is_treated', '-time_created']

    def __unicode__(self):
        reason = ""
        if self.reason:
            reason = "High"
        elif False == self.reason:
            reason = "Low"
        s = "Alarm: " + reason + " " + self.measurement.type + " at " + str(self.time_created)
        if self.measurement:
            s += " for " + self.measurement.patient.user.get_full_name()
        return smart_unicode(s)
