from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_emails(subject, message, recipient_list):
    result = send_mail(subject=subject, 
                message=message,
                from_email=settings.EMAIL_HOST_USER, 
                recipient_list=recipient_list
                  )
    return result
