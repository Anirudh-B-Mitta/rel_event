# payments/views.py
from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer

class YourPaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class YourPaymentDetailView(generics.RetrieveAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class YourTicketView(generics.ListAPIView):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        ticket_id = self.kwargs['ticket_id']
        return Payment.objects.filter(ticket=ticket_id)
    
# views.py
import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import PaymentSerializer

class PaymentView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket_id = serializer.validated_data['ticket']
        amount = serializer.validated_data['amount']

        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        # Create Razorpay order
        order_data = {
            'amount': int(amount * 100),  # Amount in paise
            'currency': 'INR',
            'payment_capture': 1  # Auto capture payment
        }
        order = client.order.create(data=order_data)

        # Store payment details in the database
        Payment.objects.create(
            ticket=ticket_id,
            PID=order['id'],
            amount=amount,
            status='success'
        )

        # Return Razorpay order ID to the front end
        return Response({'order_id': order['id']}, status=status.HTTP_201_CREATED)
