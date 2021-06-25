from django.db import models

# Create your models here.
class AccountWhitelist(models.Model):
    email = models.EmailField(unique=True)
    active = models.BooleanField()
