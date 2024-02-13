# volunteers/views.py
from rest_framework import generics
from .models import Volunteer
from .serializers import VolunteerSerializer, CombinedDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Volunteer
from broadcast.models import Broadcast
from broadcast.serializers import BroadcastSerializer
from rest_framework.permissions import IsAuthenticated


class YourVolunteerListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class YourVolunteerDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class SubscribedChannels(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        # Retrieve all broadcast channels for the given user_id
        channels = Volunteer.objects.filter(user_id=user_id).values_list('event_id', flat=True)
        # volunteers = Volunteer.objects.select_related('user', 'event', 'broadcast')
        print(channels)

        # Query the Broadcast model to get details of the subscribed channels
        subscribed_channels = Broadcast.objects.filter(event_id__in=channels).select_related('event', 'event__user')
        serializer = CombinedDataSerializer(subscribed_channels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
