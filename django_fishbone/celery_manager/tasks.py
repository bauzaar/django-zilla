# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division, absolute_import
from celery_manager.models import Job
from celery_manager.helpers import managed_task


_TASK_CATEGORY = 'MAINTENANCE'


@managed_task(category=_TASK_CATEGORY)
def vacuum_jobs():
    to_exclude = Job.objects.order_by('-id')[:20].values_list('id', flat=True)
    Job.objects.exclude(id__in=to_exclude).delete()