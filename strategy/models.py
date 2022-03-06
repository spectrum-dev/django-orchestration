import uuid
from datetime import datetime

from croniter import croniter
from django.conf import settings
from django.db import models
from django.utils import timezone


class UserStrategy(models.Model):
    class Meta:
        unique_together = ("user", "strategy")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=10
    )
    strategy = models.UUIDField(default=uuid.uuid4)
    strategy_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StrategySharing(models.Model):
    permission_types = (
        (1, "Read"),
        (2, "Write"),
    )

    strategy = models.ForeignKey(
        UserStrategy,
        related_name="%(class)s_strategy_sharing",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permissions = models.IntegerField(choices=permission_types, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Strategy(models.Model):
    class Meta:
        unique_together = ("strategy", "commit")

    strategy = models.ForeignKey(
        UserStrategy, related_name="%(class)s_strategy", on_delete=models.CASCADE
    )
    commit = models.UUIDField(default=uuid.uuid4)
    flow_metadata = models.JSONField()
    input = models.JSONField()
    output = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ScheduledStrategy(models.Model):
    strategy = models.ForeignKey(Strategy, on_delete=models.CASCADE)
    last_run_at = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    cron_expression = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        """
        function to evaluate "next_run_at" using the cron expression, so that it is updated once the report is sent.
        """
        self.last_run_at = timezone.now()
        iter = croniter(self.cron_expression, self.last_run_at)
        self.next_run_at = iter.get_next(datetime)
        super().save(*args, **kwargs)
