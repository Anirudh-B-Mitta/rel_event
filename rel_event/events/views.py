# events/views.py
from rest_framework import generics
from .models import Event
from .serializers import EventSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class YourEventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class YourEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class UserCreatedEvents(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user.id
        user_events = Event.objects.filter(user=user)
        serialized_events = EventSerializer(user_events, many=True).data
        return Response(serialized_events)
