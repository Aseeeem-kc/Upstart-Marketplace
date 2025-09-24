
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email_token = models.CharField(max_length=2000, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)

    def __str__(self):
        return self.username
