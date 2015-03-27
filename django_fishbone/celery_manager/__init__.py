# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from celery import Celery
from django.conf import settings


app = Celery(settings.CELERY_APP_NAME)

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from django_fishbone.celery_manager.signals import *