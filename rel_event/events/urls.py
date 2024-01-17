# events/urls.py
from django.urls import path
from .views import YourEventListView, YourEventDetailView, UserCreatedEvents

urlpatterns = [
    path('events/', YourEventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', YourEventDetailView.as_view(), name='event-detail'),
    path('events/self/', UserCreatedEvents.as_view(), name='user-events')
]
