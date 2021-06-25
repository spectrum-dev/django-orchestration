import uuid
from django.db import models
from django.conf import settings

# Create your models here.
class UserStrategy(models.Model):
    class Meta:
        unique_together = ("user", "strategy")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=10
    )
    strategy = models.UUIDField(default=uuid.uuid4)


class Strategy(models.Model):
    class Meta:
        unique_together = ("strategy", "commit")

    strategy = models.ForeignKey(
        UserStrategy, related_name="%(class)s_strategy", on_delete=models.PROTECT
    )
    commit = models.UUIDField(default=uuid.uuid4)
    flow_metadata = models.JSONField()
    input = models.JSONField()
    output = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
