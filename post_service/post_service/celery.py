import os

from celery import Celery

# from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "post_service.settings")
app = Celery("post_service")
# app.conf.beat_schedule = settings.CELERY_BEAT_SCHEDULE
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
