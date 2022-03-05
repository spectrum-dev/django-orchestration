from django.conf import settings
from django.db import models


class AccountWhitelist(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField()


class BasicAuthToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.TextField()
