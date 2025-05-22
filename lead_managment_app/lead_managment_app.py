import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lead_managment_app.settings')

app = Celery('lead_managment_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
