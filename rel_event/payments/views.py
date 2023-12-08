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
