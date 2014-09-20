from django.db import models


class Alarm(models.Model):
    time_created = models.DateTimeField(null=False)
    is_treated = models.BooleanField(default=False)
    treated_text = models.TextField(default="")
