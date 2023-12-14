# events/views.py
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse


class YourEventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class YourEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
