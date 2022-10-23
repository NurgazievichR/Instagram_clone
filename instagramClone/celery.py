from __future__ import absolute_import

import os
from time import sleep

from celery import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagramClone.settings')


app = Celery('instagramClone')
app.config_from_object('django.conf:settings', namespace='CELERY')




app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


