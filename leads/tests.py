from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core import mail
from django.conf import settings
from .models import Lead
import tempfile
import os

class LeadAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.temp_file = tempfile.NamedTemporaryFile(suffix='.pdf')
        self.temp_file.write(b'Mock resume content')
        self.temp_file.seek(0)

        self.lead = Lead.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            resume=SimpleUploadedFile('resume.pdf', b'Resume content')
        )

    def tearDown(self):
        self.temp_file.close()
        if self.lead.resume:
            if os.path.isfile(self.lead.resume.path):
                os.remove(self.lead.resume.path)

    def test_create_lead_public(self):
        url = reverse('lead-list')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'resume': SimpleUploadedFile('resume.pdf', b'Resume content')
        }

        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lead.objects.count(), 2)

        lead = Lead.objects.get(email='jane.smith@example.com')
        self.assertEqual(lead.first_name, 'Jane')
        self.assertEqual(lead.state, Lead.LeadState.PENDING)

        self.assertEqual(len(mail.outbox), 2)


        self.assertIn('Thank you', mail.outbox[0].subject)
        self.assertIn('jane.smith@example.com', mail.outbox[0].to)
        self.assertIn('New Lead Submission', mail.outbox[1].subject)
        self.assertIn(settings.ATTORNEY_EMAIL, mail.outbox[1].to)

    def test_list_leads_authenticated(self):
        url = reverse('lead-list')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
  

    def test_list_leads_unauthenticated(self):
        url = reverse('lead-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_mark_reached_out_action(self):
        url = reverse('lead-mark-reached-out', kwargs={'pk': self.lead.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.state, Lead.LeadState.REACHED_OUT)

    def test_download_resume(self):
        url = reverse('lead-resume', kwargs={'pk': self.lead.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Content-Disposition', response)
        self.assertTrue(response['Content-Disposition'].startswith('attachment; filename="Doe_John_resume'))
