# broadcast/urls.py
from django.urls import path
from .views import BroadcastDetailView, BroadcastListView

urlpatterns = [
    path('broadcasts/<int:pk>/', BroadcastDetailView.as_view(), name='broadcast-detail'),
    path('broadcasts/', BroadcastListView.as_view(), name='broadcast-list'),
]
