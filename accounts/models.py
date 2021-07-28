from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=21, blank=True, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)