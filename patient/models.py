from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, null=True)
    date_of_birth = models.DateField(null=False)
    telephone = models.IntegerField(default=None)
    address = models.TextField(default='')
    pulse_max = models.IntegerField(default=0)
    pulse_min = models.IntegerField(default=0)
    o2_max = models.IntegerField(default=0)
    o2_min = models.IntegerField(default=0)
    temperature_max = models.IntegerField(default=0)
    temperature_min = models.IntegerField(default=0)
    activity_max = models.IntegerField(default=0)
    activity_min = models.IntegerField(default=0)
    activity_access = models.BooleanField(default=False)
    pulse_access = models.BooleanField(default=False)
    o2_access = models.BooleanField(default=False)
    temperature_access = models.BooleanField(default=False)
