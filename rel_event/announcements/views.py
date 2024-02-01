# announcements/views.py
from rest_framework import generics
from .models import Announcement
from .serializers import AnnouncementSerializer
from rest_framework.permissions import IsAuthenticated

class YourAnnouncementDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class YourAnnouncementListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class BroadcastMessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        broadcast_id = self.kwargs['broadcast_id']
        return Announcement.objects.filter(broadcast_id=broadcast_id)