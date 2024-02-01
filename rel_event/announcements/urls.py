# announcements/urls.py
from django.urls import path
from .views import YourAnnouncementDetailView, YourAnnouncementListView, BroadcastMessageListView

urlpatterns = [
    path('announcements/<int:pk>/', YourAnnouncementDetailView.as_view(), name='announcement-detail'),
    path('announcements/', YourAnnouncementListView.as_view(), name='announcement-list'),
    path('messages/<int:broadcast_id>/', BroadcastMessageListView.as_view(), name='broadcast-announcement-list'),
]
