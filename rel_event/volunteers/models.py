# volunteers/models.py
from django.db import models
from accounts.models import CustomUser
from events.models import Event

class Volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'event')  # Ensures UID + EID is unique

    def __str__(self):
        return f"Volunteer for {self.event.event_name} ({self.user.name})"
