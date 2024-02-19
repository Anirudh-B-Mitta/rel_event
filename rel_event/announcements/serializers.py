# announcements/serializers.py
from rest_framework import serializers
from .models import Announcement
from volunteers.serializers import CombinedDataSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class BroadcastDataSerializer(serializers.ModelSerializer):
    broadcast = CombinedDataSerializer()
    class Meta:
        model = Announcement
        fields = '__all__'