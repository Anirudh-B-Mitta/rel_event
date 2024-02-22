# # accounts/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth import get_user_model

# @receiver(post_save, sender=get_user_model())
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created:
#         subject = 'Welcome to Rel-Event'
#         message = f'Hello {instance.name}, \nThank you for creating an account on Rel-Event. Let\'s party hard. We hope you enjoy your experience!'
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [instance.email]

#         send_mail(subject, message, from_email, recipient_list)

# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model

@receiver(post_save, sender=get_user_model())
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Rel-Event'
        template_name = 'accounts/welcome_email.html'
        context = {'name': instance.name, 'welcome_link': settings.FRONTEND_URL}
        
        html_message = render_to_string(template_name, context)

        email = EmailMessage(subject, '', settings.DEFAULT_FROM_EMAIL, [instance.email])
        email.content_subtype = 'html'
        email.body = html_message

        email.send()
