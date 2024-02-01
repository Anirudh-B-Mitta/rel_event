# events/views.py
from rest_framework import generics,status
from .models import Event
from .serializers import EventSerializer
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# class YourEventListView(generics.ListCreateAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer

#     def create(self, request, *args, **kwargs):
#         event_data = request.data.copy()
#         event_data['poster'] = request.data.get('poster')

#         serializer = self.get_serializer(data=event_data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)

#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        # Allow GET requests without authentication
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # Check for authentication on other request methods
        return request.user and request.user.is_authenticated


class YourEventListView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        event_data = request.data.copy()
        event_data['poster'] = request.data.get('poster')

        serializer = self.get_serializer(data=event_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class YourEventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class UserCreatedEvents(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user.id
        user_events = Event.objects.filter(user=user)
        serialized_events = EventSerializer(user_events, many=True).data
        return Response(serialized_events)
