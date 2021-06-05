from django.db import models


class BlockRegistry(models.Model):
    class Meta:
        unique_together = (("block_type", "block_id"),)

    block_type = models.CharField(max_length=32)
    block_id = models.IntegerField()
    block_name = models.CharField(max_length=128)
    inputs = models.JSONField()
    validations = models.JSONField()
