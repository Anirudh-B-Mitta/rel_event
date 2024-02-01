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
    permission_classes = [IsAuthenticated]
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

class YourTicketListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def perform_create(self, serializer):
        # Get the ticket data from the request
        ticket_data = self.request.data

        # Extract the amount from the ticket data
        amount = ticket_data.get('amount')

        # Call Razorpay API to create an order
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
