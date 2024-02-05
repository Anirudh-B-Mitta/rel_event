# payments/views.py
from rest_framework import generics
from .models import Payment
from tickets.models import Ticket
from .serializers import PaymentSerializer
from rest_framework.permissions import IsAuthenticated
import razorpay
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from django.urls import reverse
from django.shortcuts import render
from django.utils.html import strip_tags
from django.core.mail import EmailMessage

class YourPaymentListView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
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
            serializer.save()
            print("Get Successful")
            data = response.json()
            print(self.request.data)
            data['ticket_status']=get_status(self.request.data)
            response = requests.put(full_api_url, data=data)
            if response.status_code == 200:
                # The API call was successful, the resource was deleted
                print({'result': 'Ticket edited successfully'})
                print(serializer, "serializer \n", serializer.data, "serializer.data")
                self.send_creation_email(dict(serializer.data))

            else:
                # Handle errors
                print({'error': f'API call failed with status code {response.status_code}'}, status=500)
        else:
            print({'error': f'API call failed with status code {response.status_code}'}, status=500)

    def send_creation_email(self, payment_data):
        ticket_id = payment_data['ticket']
        ticket = Ticket.objects.get(pk=ticket_id)
        print(ticket.user.name)
        print(ticket.event.event_name)
        subject = f'Ticket for {ticket.event.event_name}'
        context = {'event': ticket.event, 'user': ticket.user, 'ticket': ticket, 'payment': payment_data}

        # Render the HTML content from the template
        html_message = render(self.request, 'payments/ticket_confirm.html', context).content.decode('utf-8')
        
        # Create a plain text version of the HTML content for email clients that don't support HTML
        plain_message = strip_tags(html_message)

        # Send the email
        email = EmailMessage(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [ticket.user.email])
        email.content_subtype = 'html'  # Set the content type to HTML
        email.body = html_message
        email.send()


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
    

# views.py

from django.http import JsonResponse
import razorpay

def initiate_refund(request, order_id):
    print("this is called")
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    ticket = Ticket.objects.get(order_id=order_id)
    payment = Payment.objects.get(ticket_id = ticket.TID)
    print(payment,"payment")
    print(payment.amount,"payment amount")

    try:
        refund_data = {
            'payment_id': payment.PID
        }

        refund = client.payment.refund(**refund_data)

        if refund.get('status') == 'processed':
            payment.status = 'refunded'
            payment.save()
            print(ticket.ticket_status)
            ticket.ticket_status = 'cancelled'
            ticket.save()
            return JsonResponse({'status': 'success', 'message': 'Refund processed successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Refund processing failed'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

