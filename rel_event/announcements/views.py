# announcements/views.py
from rest_framework import generics
from .models import Announcement
from .serializers import AnnouncementSerializer

class YourAnnouncementDetailView(generics.RetrieveDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class YourAnnouncementListView(generics.ListCreateAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class BroadcastMessageListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer

    def get_queryset(self):
        broadcast_id = self.kwargs['broadcast_id']
        return Announcement.objects.filter(broadcast_id=broadcast_id)