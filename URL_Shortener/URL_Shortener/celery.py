import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "URL_Shortener.settings")

app = Celery("URL_Shortener")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()