from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode


class Patient(models.Model):
    hub = models.OneToOneField(User, null=True, blank=True, related_name='hub_patient')
    user = models.OneToOneField(User, null=True)
    national_identification_number = models.CharField(
        default="",
        max_length=11,
        help_text="A number consisting of date of birth + national id, (11 digits)"
    )
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=4, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
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
