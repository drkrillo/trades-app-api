"""
Celery file for scheduled tasks.
"""
import os

from celery import Celery


# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# you can change the name here
app = Celery("app", broker='redis://redis:6379/0')

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# discover and load tasks.py from from all registered Django apps
app.autodiscover_tasks()
