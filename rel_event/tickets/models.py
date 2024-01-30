# tickets/models.py
from django.db import models
from accounts.models import CustomUser
from events.models import Event

class Ticket(models.Model):
    TID = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    num_people = models.IntegerField()
    attending = models.IntegerField()
    order_id = models.CharField(max_length=20)

    def __str__(self):
        return f"Ticket {self.TID} for {self.user} at {self.event}"
