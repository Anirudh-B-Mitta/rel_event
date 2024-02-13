# volunteers/serializers.py
from rest_framework import serializers
from .models import Volunteer

class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'

# volunteers/serializers.py
from rest_framework import serializers
from events.models import Event
from accounts.serializers import UserSerializer
from broadcast.models import Broadcast
# from .models import Volunteers

class EventUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Event
        fields = '__all__'

class CombinedDataSerializer(serializers.ModelSerializer):
    event = EventUserSerializer()

    class Meta:
        model = Broadcast
        fields = '__all__'
