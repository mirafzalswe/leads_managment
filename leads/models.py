from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Lead(models.Model):
    class LeadState(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        REACHED_OUT = 'REACHED_OUT', _('Reached Out')

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    state = models.CharField(max_length=20, choices=LeadState.choices, default=LeadState.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
