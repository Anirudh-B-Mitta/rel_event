# events/views.py
from rest_framework import generics,status
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

    def create(self, request, *args, **kwargs):
        event_data = request.data.copy()  # Copy the request data to modify it
        event_data['poster'] = request.data.get('poster')  # Add the poster file to the data

        serializer = self.get_serializer(data=event_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
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
