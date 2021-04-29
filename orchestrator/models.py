import uuid
from django.db import models

# Create your models here.

class BlockRegistry(models.Model):
    class Meta:
        unique_together = (('block_type', 'block_id'),)

    block_type = models.CharField(max_length=32)
    block_id = models.IntegerField()
    block_name = models.CharField(max_length=128)
    inputs = models.JSONField()
    validations = models.JSONField()

# class Strategy(models.Model):
#     class Meta:
#         unique_together = (('strategy_id', 'commit_id'))
#
#     strategy_id = models.UUIDField(default=uuid.uuid4, editable=False)
#     commit_id = models.UUIDField(default=uuid.uuid4, editable=False)
#     flow_metadata = models.JSONField()
#     input = models.JSONField()
#     ouput = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
