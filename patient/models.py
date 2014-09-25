from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, null=True)
    national_identification_number = models.PositiveSmallIntegerField(
        max_length=11, help_text=
        "A number consisting of date of birth + national id, called fødselsnummer, needs to be 11 digits long")
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
    activity_access = models.BooleanField(
        default=False, help_text="If True, the patient has access to view activity data in patient interface")
    pulse_access = models.BooleanField(
        default=False, help_text="If True, the patient has access to view pulse data in patient interface")
    o2_access = models.BooleanField(
        default=False, help_text="If True, the patient has access to view o2 data in patient interface")
    temperature_access = models.BooleanField(
        default=False, help_text="If True, the patient has access to view temperature data in patient interface")
