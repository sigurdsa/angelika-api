from django.db import models
from patient.models import Patient
from django.utils.encoding import smart_unicode


class NextOfKin(models.Model):
    patient = models.ForeignKey(Patient, null=False)
    first_name = models.CharField(null=False, max_length=80)
    last_name = models.CharField(null=False, max_length=80)
    address = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    priority = models.IntegerField(default=0, null=False)
    relation = models.CharField(null=True, max_length=40, blank=True)

    def __unicode__(self):
        name = self.first_name + " " + self.last_name
        return smart_unicode(name)
