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
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .serializers import PaymentSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST



class PaymentView(APIView):
    @csrf_exempt
    @require_POST
    def post(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ticket = serializer.validated_data['ticket']
        amount = serializer.validated_data['amount']

        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create Razorpay order
        order_data = {
            'amount': int(amount * 100),  # Amount in paise
            'currency': 'INR',
            'payment_capture': 1  # Auto capture payment
        }
        order = client.order.create(order_data)
        print(order)

        # Store payment details in the database
        payment = Payment.objects.create(
            ticket=ticket,
            PID=order['id'],
            amount=amount,
            status='Success'
        )

        # Return Razorpay order ID to the front end
        return Response({'order_id': order['id']}, status=status.HTTP_201_CREATED)
