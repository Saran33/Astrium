from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from  django.conf import settings
# from pytz import timezone
# from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'astrium.settings')

app = Celery('astrium')
app.conf.enable_utc = True
app.conf.update(timezone='UTC')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'every-10-seconds' : {
        'task':  'main_app.tasks.update_security',
        'schedule': 10,
        'args': (['AAPL', 'AMZN', 'FB'],)
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(F'Request: {self.request!r}')