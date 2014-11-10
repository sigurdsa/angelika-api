from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode


class Patient(models.Model):
    hub = models.OneToOneField(User, null=True, blank=True, related_name='hub_patient')
    user = models.OneToOneField(User, null=True)
    national_identification_number = models.CharField(
        default="",
        max_length=11,
        unique=True,
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

    show_activity = models.BooleanField(
        default=True,
        help_text="If True, activity data is shown in the interface for health professionals"
    )
    show_pulse = models.BooleanField(
        default=True,
        help_text="If True, heart rate data is shown in the interface for health professionals"
    )
    show_o2 = models.BooleanField(
        default=True,
        help_text="If True, O2 data is shown in the interface for health professionals"
    )
    show_temperature = models.BooleanField(
        default=True,
        help_text="If True, temperature data is shown in the interface for health professionals"
    )

    def __unicode__(self):
        name = self.user.get_full_name()
        if len(name) <= 2:
            name = self.user.username
        return smart_unicode(name)
