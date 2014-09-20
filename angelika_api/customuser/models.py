from django.db import models


from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUser(AbstractBaseUser):
    identifier = models.CharField(max_length=40, unique=True)
    patient = models.ForeignKey('patient.Patient')
    USERNAME_FIELD = 'identifier'