from django.db import models


class Alarm(models.Model):
    time_created = models.DateTimeField(null=False)
    is_treated = models.BooleanField(default=False, null=False)
    treated_text = models.TextField(default="", blank=True)
