from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, MaxValueValidator
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.

class Lead(models.Model):
    class LeadState(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        REACHED_OUT = 'REACHED_OUT', _('Reached Out')

    first_name = models.CharField(max_length=20, db_index=True)
    last_name = models.CharField(max_length=20, db_index=True)
    email = models.EmailField(max_length=100, db_index=True)
    resume = models.FileField(
        upload_to='resumes/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx']),
            MaxValueValidator(settings.MAX_UPLOAD_SIZE)
        ]
    )
    state = models.CharField(
        max_length=20,
        choices=LeadState.choices,
        default=LeadState.PENDING,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['state', 'created_at']),
            models.Index(fields=['email', 'state']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super().clean()
        if self.resume and self.resume.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError({
                'resume': f'File size must be no more than {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB'
            })
