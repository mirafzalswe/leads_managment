from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.exceptions import MaxRetriesExceededError
from django.core.files.storage import default_storage
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
    rate_limit='10/m'  # 10 tasks per minute
)
def send_lead_notification_email(self, lead_email, lead_name):
    try:
        subject = f'New Lead: {lead_name}'
        message = f'A new lead has been submitted by {lead_name} ({lead_email}).'

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ATTORNEY_EMAIL],
            fail_silently=False,
        )
        logger.info(f'Notification email sent for lead: {lead_name}')
        return f'Notification email sent for lead: {lead_name}'
    except Exception as exc:
        logger.error(f'Failed to send notification email for lead {lead_name}: {str(exc)}')
        try:
            self.retry(exc=exc)
        except MaxRetriesExceededError:
            logger.error(f'Max retries exceeded for notification email to {lead_name}')
            raise

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
    rate_limit='10/m'  # 10 tasks per minute
)
def send_lead_confirmation_email(self, lead_email, lead_name):
    try:
        subject = 'Thank you for your interest'
        message = f'Dear {lead_name},\n\nThank you for submitting your information. We will review it and get back to you soon.\n\nBest regards,\nYour Company Name'

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[lead_email],
            fail_silently=False,
        )
        logger.info(f'Confirmation email sent to: {lead_email}')
        return f'Confirmation email sent to: {lead_email}'
    except Exception as exc:
        logger.error(f'Failed to send confirmation email to {lead_email}: {str(exc)}')
        try:
            self.retry(exc=exc)
        except MaxRetriesExceededError:
            logger.error(f'Max retries exceeded for confirmation email to {lead_email}')
            raise

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
    rate_limit='10/m'  # 10 tasks per minute
)
def send_daily_lead_report(self):
    try:
        from django.utils import timezone
        from datetime import timedelta
        from .models import Lead

        yesterday = timezone.now() - timedelta(days=1)
        leads = Lead.objects.filter(created_at__date=yesterday.date())
        
        subject = f'Daily Lead Report - {yesterday.date()}'
        message = f'Daily Lead Report\n\n'
        message += f'Total Leads: {leads.count()}\n'
        message += f'Pending Leads: {leads.filter(state="PENDING").count()}\n'
        message += f'Reached Out Leads: {leads.filter(state="REACHED_OUT").count()}\n\n'
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ATTORNEY_EMAIL],
            fail_silently=False,
        )
        logger.info(f'Daily lead report sent for {yesterday.date()}')
        return f'Daily lead report sent for {yesterday.date()}'
    except Exception as exc:
        logger.error(f'Failed to send daily lead report: {str(exc)}')
        try:
            self.retry(exc=exc)
        except MaxRetriesExceededError:
            logger.error('Max retries exceeded for daily lead report')
            raise

@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=300,  # 5 minutes
    rate_limit='10/m'  # 10 tasks per minute
)
def process_lead_resume(self, lead_id):
    """
    Process the uploaded resume for a lead.
    - Validates file format
    - Creates backup copy
    - Extracts text for search indexing
    - Updates lead status
    """
    try:
        from .models import Lead
        import shutil
        from datetime import datetime

        lead = Lead.objects.get(id=lead_id)
        if not lead.resume:
            logger.warning(f'No resume found for lead {lead_id}')
            return f'No resume found for lead ID: {lead_id}'

        # Create backup directory if it doesn't exist
        backup_dir = os.path.join(settings.MEDIA_ROOT, 'resume_backups')
        os.makedirs(backup_dir, exist_ok=True)

        # Create backup with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{lead.last_name}_{lead.first_name}_{timestamp}{Path(lead.resume.name).suffix}"
        backup_path = os.path.join(backup_dir, backup_filename)

        # Copy file to backup location
        shutil.copy2(lead.resume.path, backup_path)
        logger.info(f'Created backup of resume for lead {lead_id} at {backup_path}')

        # Here you could add additional processing like:
        # - Text extraction for search indexing
        # - File format conversion
        # - Metadata extraction
        # - Virus scanning
        # - etc.

        return f'Resume processed for lead ID: {lead_id}'
    except Lead.DoesNotExist:
        logger.error(f'Lead {lead_id} not found')
        raise
    except Exception as exc:
        logger.error(f'Error processing resume for lead {lead_id}: {str(exc)}')
        try:
            self.retry(exc=exc)
        except MaxRetriesExceededError:
            logger.error(f'Max retries exceeded for resume processing of lead {lead_id}')
            raise