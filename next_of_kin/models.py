from django.db import models
from patient.models import Patient
from django.utils.encoding import smart_unicode


class NextOfKin(models.Model):
    patient = models.ForeignKey(Patient, null=False)
    full_name = models.CharField(null=False, blank=False, max_length=160)
    address = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=False)
    priority = models.IntegerField(default=0, null=False)
    relation = models.CharField(null=True, max_length=40, blank=False)

    def __unicode__(self):
        s = self.full_name + ", med relasjon " +\
            self.relation + " til " + self.patient.user.get_full_name()
        return smart_unicode(s)

    class Meta():
        ordering = ['priority']
