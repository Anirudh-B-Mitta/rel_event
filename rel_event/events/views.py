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

def send_email_to_customer(request):
    subject = "Test"
    message = "Hi This is test from Django"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["rohithburle16@gmail.com","chitra17.mahadev@gmail.com"]
    send_mail(subject, message, from_email, recipient_list)
    return HttpResponse('Email sent successfully!')
 