# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from celery.signals import task_prerun, task_postrun, task_success, task_failure, before_task_publish
from celery import states
from django.core.exceptions import ObjectDoesNotExist
from kombu.utils.encoding import safe_repr
from django_fishbone import transaction_handler
from django_fishbone.celery_manager.models import Job
from django_fishbone.utils.datetime_utils import get_utc_now


def _simplify_task_name(task_name):
    return '.'.join(task_name.split('.')[-3:])


@before_task_publish.connect
def before_task_publish_handler(body, *options, **kwoptions):
    with transaction_handler():
        task_name = _simplify_task_name(body['task'])
        headers = kwoptions['headers']
        task_id = body['id']
        if not Job.objects.filter(task_id=task_id).exists():
            Job.objects.create(task=task_name, args=safe_repr(body['args']), kwargs=safe_repr(body['kwargs']),
                               task_id=task_id, state=states.PENDING, category=headers['category'],
                               scheduled=headers.get('scheduled', False))


@task_prerun.connect
def prerun_handler(sender, task, task_id, args, kwargs, *options, **kwoptions):
    with transaction_handler():
        try:
            job_Locked = Job.objects.select_for_update().get(task_id=task_id)
        except Job.DoesNotExist:  # in case of local run: apply()
            job_Locked = Job.objects.select_for_update().create(
                task=_simplify_task_name(task.name), args=safe_repr(args), kwargs=safe_repr(kwargs),
                task_id=task_id, category=task.category
            )
        job_Locked.state = states.STARTED
        job_Locked.timestamp_prerun = get_utc_now()
        job_Locked.save()


@task_postrun.connect
def postrun_handler(sender, task, task_id, signal, state, retval, *args, **kwargs):
    with transaction_handler():
        try:
            job_Locked = Job.objects.select_for_update().get(task_id=task_id)
        except Job.DoesNotExist:
            raise ObjectDoesNotExist
        job_Locked.state = state
        job_Locked.timestamp_postrun = get_utc_now()
        job_Locked.save()


@task_success.connect
def success_handler(sender, result, *args, **kwargs):
    with transaction_handler():
        try:
            job_Locked = Job.objects.select_for_update().get(task_id=sender.request.id)
        except Job.DoesNotExist:
            raise ObjectDoesNotExist
        job_Locked.result = safe_repr(result) or ''
        job_Locked.save()


@task_failure.connect
def failure_handler(sender, task_id, exception, traceback, einfo, *args, **kwargs):
    with transaction_handler():
        try:
            job_Locked = Job.objects.select_for_update().get(task_id=task_id)
        except Job.DoesNotExist:
            raise ObjectDoesNotExist
        job_Locked.result = einfo.traceback
        job_Locked.save()