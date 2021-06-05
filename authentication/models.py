from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class AccountWhitelist(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField()
