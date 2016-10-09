# coding=utf-8
from __future__ import absolute_import

import os
import sys
from os.path import abspath, dirname

from celery import Celery
from django.conf import settings

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.prod')

# Create celery app instance that should be used everywhere in the code
app = Celery('app.celery.celery')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
