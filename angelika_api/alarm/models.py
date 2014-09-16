from django.db import models


class Alarm(models.Model):
    time_created = models.DateTimeField(null=False)
