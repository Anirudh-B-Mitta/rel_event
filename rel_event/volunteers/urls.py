# volunteers/urls.py
from django.urls import path
from .views import SubscribedChannels, YourVolunteerListView, YourVolunteerDetailView, VolunteerAPIView, VolunteerCount  # Replace with your views

urlpatterns = [
    path('volunteers/', YourVolunteerListView.as_view(), name='volunteer-list'),
    path('volunteers/<int:pk>/', YourVolunteerDetailView.as_view(), name='volunteer-detail'),
    path('self-channels/<int:user_id>/', SubscribedChannels.as_view(), name='subscribed-channels'),
    path('getVID/<int:event_id>/', VolunteerAPIView.as_view(), name='get-VID'),
    path('num-volunteers/<int:event_id>/', VolunteerCount.as_view(), name='get-v_count'),
    # Add more URL patterns as needed
]
