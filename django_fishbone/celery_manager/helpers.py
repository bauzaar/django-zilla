# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from celery import shared_task
from django_fishbone.celery_manager.base_task import ManagedTask


def managed_task(*args, **kwargs):
    return shared_task(base=ManagedTask, *args, **kwargs)