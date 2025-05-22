from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

# ... existing code ...

@shared_task
def send_lead_notification_email(lead_email, lead_name):
    subject = f'New Lead: {lead_name}'
    message = f'A new lead has been submitted by {lead_name} ({lead_email}).'

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ATTORNEY_EMAIL],
        fail_silently=False,
    )
    return f'Notification email sent for lead: {lead_name}'

@shared_task
def send_lead_confirmation_email(lead_email, lead_name):
    subject = 'Thank you for your interest'
    message = f'Dear {lead_name},\n\nThank you for submitting your information. We will review it and get back to you soon.\n\nBest regards,\nYour Company Name'

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[lead_email],
        fail_silently=False,
    )
    return f'Confirmation email sent to: {lead_email}'

@shared_task
def process_lead_resume(lead_id):
    """Process the uploaded resume for a lead."""
    return f'Resume processed for lead ID: {lead_id}'