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
from django.shortcuts import render
from django.utils.html import strip_tags
from django.core.mail import EmailMessage

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
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        event_data = request.data.copy()
        event_data['poster'] = request.data.get('poster')

        serializer = self.get_serializer(data=event_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        self.send_creation_email(serializer.instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def send_creation_email(self, event):
        user = event.user
        print(user.name)
        print(event.poster)
        subject = 'Event Created Successfully'
        context = {'event': event, 'name': user.name}

        # Render the HTML content from the template
        html_message = render(self.request, 'events/creation_email.html', context).content.decode('utf-8')
        
        # Create a plain text version of the HTML content for email clients that don't support HTML
        plain_message = strip_tags(html_message)

        # Send the email
        email = EmailMessage(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email])
        email.content_subtype = 'html'  # Set the content type to HTML
        email.body = html_message
        email.send()

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
