# volunteers/views.py
from rest_framework import generics
from .models import Volunteer
from .serializers import VolunteerSerializer, CombinedDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Volunteer
from broadcast.models import Broadcast
from rest_framework.permissions import IsAuthenticated
from events.models import Event


class YourVolunteerListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class YourVolunteerDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class SubscribedChannels(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        channels = Volunteer.objects.filter(user_id=user_id).values_list('event_id', flat=True)

        subscribed_channels = Broadcast.objects.filter(event_id__in=channels).select_related('event', 'event__user')
        serializer = CombinedDataSerializer(subscribed_channels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class VolunteerAPIView(APIView):
    def get(self, request, event_id):
        # Authenticate user based on the provided token
        user = request.user

        if not user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the event based on the provided event ID
        try:
            event = Event.objects.get(EID=event_id)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if a volunteer entry already exists for the user and event
        try:
            volunteer = Volunteer.objects.get(user=user, event=event)
            print(volunteer, "volunteer")
            print(volunteer.id, "volunteer id")
            vid = volunteer.id
            return Response({"vid": vid}, status=status.HTTP_200_OK)
        except Volunteer.DoesNotExist:
            # If no volunteer entry exists, create a new one
            volunteer = Volunteer.objects.create(user=user, event=event)
            vid = volunteer.id
            return Response({"vid": vid}, status=status.HTTP_201_CREATED)

class VolunteerCount(APIView):
    def get(self, request, event_id):
        v_count = Volunteer.objects.filter(event_id=event_id).count()
        return Response(v_count, status=status.HTTP_200_OK)