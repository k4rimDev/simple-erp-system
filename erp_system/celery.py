from __future__ import absolute_import, unicode_literals

import os
import logging

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger("Celery")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_system.settings')

app = Celery('config')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    ...
}

# Development Settings
if not settings.DEBUG:
    app.conf.update(
        BROKER_URL='redis://:{password}@localhost:6379/0'.format(password="EJZKK7foRij2rxTA"),
        CELERYBEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler',
        CELERY_RESULT_BACKEND='redis://:{password}@redis:6379/1'.format(password="EJZKK7foRij2rxTA"),
        CELERY_DISABLE_RATE_LIMITS=True,
        CELERY_ACCEPT_CONTENT=['json', ],
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        CELERY_IMPORTS = ("core.tasks", )
    )

# Production Settings
else:
    app.conf.update(
        BROKER_URL='redis://:{password}@redis:{port}/0'.format(
            password=os.getenv("REDIS_PASSWORD"), 
            port=os.getenv("REDIS_PORT"),
        ),
        CELERY_RESULT_BACKEND='redis://:{password}@redis:{port}/1'.format(
            password=os.getenv("REDIS_PASSWORD"), 
            port=os.getenv("REDIS_PORT"),
        ),
        CELERY_DISABLE_RATE_LIMITS=True,
        CELERY_ACCEPT_CONTENT=['json', ],
        CELERY_TASK_SERIALIZER='json',
        CELERY_RESULT_SERIALIZER='json',
        CELERY_IMPORTS = ("core.tasks", )
    )
