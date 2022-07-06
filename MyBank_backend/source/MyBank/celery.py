import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyBank.settings')

app = Celery('MyBank')
# app.setup_security()
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()