# volunteers/views.py
from rest_framework import generics
from .models import Volunteer
from .serializers import VolunteerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Volunteer
from broadcast.models import Broadcast
from broadcast.serializers import BroadcastSerializer 


class YourVolunteerListView(generics.ListCreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class YourVolunteerDetailView(generics.RetrieveDestroyAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class SubscribedChannels(APIView):
    def get(self, request, user_id):
        # Retrieve all broadcast channels for the given user_id
        channels = Volunteer.objects.filter(user_id=user_id).values_list('event_id', flat=True)
        print(channels)

        # Query the Broadcast model to get details of the subscribed channels
        subscribed_channels = Broadcast.objects.filter(event_id__in=channels)
        serializer = BroadcastSerializer(subscribed_channels, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
