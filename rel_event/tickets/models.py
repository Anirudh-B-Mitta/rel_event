# tickets/models.py
from django.db import models
from accounts.models import CustomUser
from events.models import Event

class Ticket(models.Model):
    TID = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    num_people = models.IntegerField()
    order_id = models.CharField(max_length=20)
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('not_paid', 'Not Paid'),
        ('fail', 'Fail'),
        ('cancelled', 'Cancelled'),
    )
    ticket_status = models.CharField(max_length=20, default='not_paid', choices=STATUS_CHOICES)

    def __str__(self):
        return f"Ticket {self.TID} for {self.user} at {self.event}"
