# tickets/views.py
from rest_framework import generics
from .models import Ticket
from .serializers import TicketSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer
import razorpay
from django.conf import settings
from rest_framework.permissions import IsAuthenticated

class YourTicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class UserTicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Ticket.objects.filter(user_id=user_id)

class EventTicketListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Ticket.objects.filter(event_id=event_id)

# class YourTicketListView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer

#     def perform_create(self, serializer):
#         # Get the ticket data from the request
#         ticket_data = self.request.data

#         # Extract the amount from the ticket data
#         amount = ticket_data.get('amount')

#         # Call Razorpay API to create an order
#         order_id = create_razorpay_order(amount)

#         # Save the ticket object to the database
#         serializer.save(order_id=order_id)

#         return Response({'order_id': order_id}, status=status.HTTP_201_CREATED)

# def create_razorpay_order(amount):
#     # Initialize the Razorpay client with your API key and secret
#     client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    

#     # Create an order with the specified amount
#     order_params = {
#         'amount': amount * 100,  # Razorpay expects the amount in paise
#         'currency': 'INR',       # Change the currency based on your requirements
#         'payment_capture': 1     # Auto capture the payment
#     }

#     order = client.order.create(data=order_params)

#     # Return the order ID
#     return order['id']

# tickets/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Ticket
from .serializers import TicketSerializer
import razorpay
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
import requests
from django.urls import reverse

class YourTicketListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        user_id = self.request.data.get('user')
        event_id = self.request.data.get('event')

        # Check if a ticket with the given user_id and event_id already exists
        existing_ticket = Ticket.objects.filter(user_id=user_id, event_id=event_id).last()
        print(existing_ticket)

        if existing_ticket:
            # If the ticket exists, check its status
            if existing_ticket.ticket_status == 'not_paid':
                print(existing_ticket.ticket_status)
                api_url = reverse('ticket-detail', kwargs={'pk': existing_ticket.TID})
                full_api_url = self.request.build_absolute_uri(api_url)
                response = requests.delete(full_api_url)
                if response.status_code == 204:
                    # The API call was successful, the resource was deleted
                    print({'result': 'Ticket deleted successfully'})
                else:
                    # Handle errors
                    print({'error': f'API call failed with status code {response.status_code}'}, status=500)

            # If the ticket is paid, create a new order
            amount = self.request.data.get('amount')
            order_id = create_razorpay_order(amount)
        else:
            # If the ticket doesn't exist, create a new order
            amount = self.request.data.get('amount')
            order_id = create_razorpay_order(amount)

        # Save the ticket object to the database
        serializer.save(order_id=order_id)

        return Response({'order_id': order_id}, status=status.HTTP_201_CREATED)

def create_razorpay_order(amount):
    # Initialize the Razorpay client with your API key and secret
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

    # Create an order with the specified amount
    order_params = {
        'amount': amount * 100,  # Razorpay expects the amount in paise
        'currency': 'INR',       # Change the currency based on your requirements
        'payment_capture': 1     # Auto capture the payment
    }

    order = client.order.create(data=order_params)

    # Return the order ID
    return order['id']
