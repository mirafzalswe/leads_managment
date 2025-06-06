from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.http import FileResponse
from .models import Lead
from django.core.mail import send_mail
from .serializers import (
    LeadCreateSerializer,
    LeadListSerializer,
    LeadDetailSerializer,
    LeadStateUpdateSerializer,
)
from .tasks import send_lead_confirmation_email, send_lead_notification_email


class IsPublicCreateOrIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return request.user and request.user.is_authenticated


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    permission_classes = [IsPublicCreateOrIsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return LeadCreateSerializer
        elif self.action == 'list':
            return LeadListSerializer
        elif self.action == 'mark_reached_out':
            return LeadStateUpdateSerializer
        return LeadDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        lead = serializer.save()
        # ordinary version
        self._send_prospect_email(lead)
        self._send_attorney_email(lead) 
        # send_prospect_email_task.delay(lead.first_name, lead.email) 
        # send_attorney_email_task.delay(lead.first_name, lead.last_name, lead.email) 

        #  Celery version
        # lead_name = f"{lead.first_name} {lead.last_name}"
        # send_lead_confirmation_email.delay(lead.email, lead_name)
        # send_lead_notification_email.delay(lead.email, lead_name)


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def _send_prospect_email(self, lead):
        """Send a confirmation email to the prospect."""
        subject = 'Thank you for your submission'
        message = f'Dear {lead.first_name},\n\nThank you for submitting your information. Our team will review your submission and contact you soon.\n\nBest regards,\nThe Team'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [lead.email],
            fail_silently=False,
        )
    
    def _send_attorney_email(self, lead):
        """Send a notification email to the attorney."""
        subject = 'New Lead Submission'
        message = f'A new lead has been submitted:\n\nName: {lead.first_name} {lead.last_name}\nEmail: {lead.email}\n\nPlease check the lead management system for more details.'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ATTORNEY_EMAIL],
            fail_silently=False,
        )
    

    @action(detail=True, methods=['get'])
    def resume(self, request, pk=None):
        lead = self.get_object()
        if lead.resume:
            return FileResponse(
                lead.resume.open('rb'),
                as_attachment=True,
                filename=f"{lead.last_name}_{lead.first_name}_resume{lead.resume.name[lead.resume.name.rfind('.'):]}"
            )
        return Response({'detail': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def mark_reached_out(self, request, pk=None):
        lead = self.get_object()
        lead.state = 'REACHED_OUT'
        lead.save()
        return Response({'status': 'Lead marked as REACHED_OUT'})

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

  