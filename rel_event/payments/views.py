# payments/views.py
from rest_framework import generics
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
import razorpay
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django.urls import reverse

class YourPaymentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        
        def get_status(res):
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

            # Verify the payment
            try:
                params_dict = {
                    'razorpay_payment_id': res['PID'],
                    'razorpay_order_id': res['order_id'],
                    'razorpay_signature': res['signature'],
                }
                client.utility.verify_payment_signature(params_dict)
                # If verification is successful, mark the payment as successful in your database
                return 'success'
            except Exception as e:
                # Handle verification failure
                return 'failure'

        ticket_id = self.request.data.get('ticket')
        api_url = reverse('ticket-detail', kwargs={'pk': ticket_id})
        full_api_url = self.request.build_absolute_uri(api_url)
        # data = {'ticket_status': self.request.data.status}
        response = requests.get(full_api_url)
        print(response)
        if response.status_code == 200:
            print("Get Successful")
            data = response.json()
            print(self.request.data)
            data['ticket_status']=get_status(self.request.data)
            response = requests.put(full_api_url, data=data)
            if response.status_code == 200:
                # The API call was successful, the resource was deleted
                print({'result': 'Ticket edited successfully'})
            else:
                # Handle errors
                print({'error': f'API call failed with status code {response.status_code}'}, status=500)
        else:
            print({'error': f'API call failed with status code {response.status_code}'}, status=500)

class YourPaymentDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class YourTicketView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def get_queryset(self):
        ticket_id = self.kwargs['ticket_id']
        return Payment.objects.filter(ticket=ticket_id)
    

# class PaymentView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request, *args, **kwargs):
#         serializer = PaymentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         ticket_id = serializer.validated_data['ticket']
#         amount = serializer.validated_data['amount']

#         # Initialize Razorpay client
#         client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

#         # Create Razorpay order
#         order_data = {
#             'amount': int(amount * 100),  # Amount in paise
#             'currency': 'INR',
#             'payment_capture': 1  # Auto capture payment
#         }
#         order = client.order.create(data=order_data)

#         # Store payment details in the database
#         Payment.objects.create(
#             ticket=ticket_id,
#             PID=order['id'],
#             amount=amount,
#             status='success'
#         )

#         # Return Razorpay order ID to the front end
#         return Response({'order_id': order['id']}, status=status.HTTP_201_CREATED)
