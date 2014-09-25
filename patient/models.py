from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, null=True)
    date_of_birth = models.DateField(null=False)
    telephone = models.IntegerField(default=None)
    normal_pulse_max = models.IntegerField(default=0)
    normal_pulse_min = models.IntegerField(default=0)
    normal_o2 = models.IntegerField(default=0)
    normal_temperature_max = models.IntegerField(default=0)
    normal_temperature_min = models.IntegerField(default=0)
    normal_activity = models.IntegerField(default=0)
