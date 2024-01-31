# volunteers/urls.py
from django.urls import path
from .views import SubscribedChannels, YourVolunteerListView, YourVolunteerDetailView  # Replace with your views

urlpatterns = [
    path('volunteers/', YourVolunteerListView.as_view(), name='volunteer-list'),
    path('volunteers/<int:pk>/', YourVolunteerDetailView.as_view(), name='volunteer-detail'),
    path('self-channels/<int:user_id>/', SubscribedChannels.as_view(), name='subscribed-channels'),
    # Add more URL patterns as needed
]
