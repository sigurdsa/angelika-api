from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode


class Patient(models.Model):
    hub_id = models.CharField(max_length=12, null=True)
    user = models.OneToOneField(User, null=True)
    national_identification_number = models.CharField(
        default="",
        max_length=11,
        help_text="A number consisting of date of birth + national id, (11 digits)"
    )
    telephone = models.IntegerField(default=None)
    address = models.TextField(default='')
    pulse_max = models.FloatField(default=0)
    pulse_min = models.FloatField(default=0)
    o2_max = models.FloatField(default=0)
    o2_min = models.FloatField(default=0)
    temperature_max = models.FloatField(default=0)
    temperature_min = models.FloatField(default=0)
    activity_access = models.BooleanField(
        default=False,
        help_text="If True, the patient has access to view activity data in patient interface"
    )
    pulse_access = models.BooleanField(
        default=False,
        help_text="If True, the patient has access to view pulse data in patient interface"
    )
    o2_access = models.BooleanField(
        default=False,
        help_text="If True, the patient has access to view o2 data in patient interface")
    temperature_access = models.BooleanField(
        default=False,
        help_text="If True, the patient has access to view temperature data in patient interface"
    )

    def __unicode__(self):
        name = self.user.first_name + " " + self.user.last_name
        if len(name) <= 2:
            name = self.user.username
        return smart_unicode(name)
