# events/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import Event
from broadcast.models import Broadcast

# automatic broadcast channel if event is created
@receiver(post_save, sender=Event)
def create_broadcast(sender, instance, created, **kwargs):
    if created:
        Broadcast.objects.create(event=instance, broadcast_name=f"{instance.event_name} Broadcast")
