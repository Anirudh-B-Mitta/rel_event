# payments/models.py
from django.db import models
from tickets.models import Ticket

class Payment(models.Model):
    PID = models.CharField(primary_key=True, max_length=200)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
        ('success', 'Success'),
        ('fail', 'Fail'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.PID} for Ticket {self.ticket.TID} ({self.status})"
