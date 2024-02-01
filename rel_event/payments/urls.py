# payments/urls.py
from django.urls import path
from .views import YourPaymentListView, YourPaymentDetailView, YourTicketView

urlpatterns = [
    path('payments/', YourPaymentListView.as_view(), name='payment-list'),
    path('payments/<str:pk>/', YourPaymentDetailView.as_view(), name='payment-detail'),
    path('tickets/<int:ticket_id>/payment/', YourTicketView.as_view(), name='ticket-view'),
    # path('pay-now/', PaymentView.as_view(), name='payment-api'),
]
