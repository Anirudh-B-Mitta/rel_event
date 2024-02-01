# broadcast/views.py
from rest_framework import generics
from .models import Broadcast
from .serializers import BroadcastSerializer
from rest_framework.permissions import IsAuthenticated


class BroadcastDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer

class BroadcastListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer