# tickets/urls.py
from django.urls import path
from .views import YourTicketListView, YourTicketDetailView, UserTicketListView, EventTicketListView  # Replace with your views

urlpatterns = [
    path('tickets/', YourTicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', YourTicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/user/<int:user_id>/', UserTicketListView.as_view(), name='user-tickets'),
    path('tickets/event/<int:event_id>/', EventTicketListView.as_view(), name='event-tickets'),

    # Add more URL patterns as needed
]
