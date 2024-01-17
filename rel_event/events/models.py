from django.db import models
from accounts.models import CustomUser

class Event(models.Model):
    EID = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    startDate = models.DateField()
    endDate = models.DateField()
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=13, decimal_places=10)
    longitude = models.DecimalField(max_digits=13, decimal_places=10)
    time = models.TimeField()
    require_volunteers = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='event_posters/', null=True, blank=True)
    ticket_cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=510, null =True) 
    medium_choices=(("offline","Offline"),("online","Online"))
    medium = models.CharField(max_length=10, choices=medium_choices,default="offline")
    category_choices=(("music","Music"),
        ("games","Games"),
        ("sports","Sports"),
        ("arts","Arts"),
        ("film","Film"),
        ("literature","Literature"),
        ("technology","Technology"),
        ("other","Other")
    )
    category = models.CharField(max_length=10, choices=category_choices,default="other")
    duration = models.DecimalField(max_digits=4,decimal_places=2,null =True)
    privacy = models.BooleanField(default=False)

    def __str__(self):
        return self.event_name

