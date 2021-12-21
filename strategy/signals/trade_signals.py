from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Trade


@receiver(post_save, sender=Trade)
def trade_saved(sender, **kwargs):
    print("trade signal called successfully")
    ## Trigger some API run here
    ## Notifications telegram etc.
