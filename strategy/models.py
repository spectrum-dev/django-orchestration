import uuid
from django.db import models

# Create your models here.


class Strategy(models.Model):
    class Meta:
        unique_together = ("strategy_id", "commit_id")

    strategy_id = models.UUIDField(default=uuid.uuid4)
    commit_id = models.UUIDField(default=uuid.uuid4)
    flow_metadata = models.JSONField()
    input = models.JSONField()
    output = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
