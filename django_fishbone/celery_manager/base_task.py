# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from celery import Task
from django.conf import settings
from django_fishbone import transaction_handler


def _partition(iterable, n):
    iterable_len = len(iterable)
    if iterable_len > n:
        r = iterable_len / n
        for i in xrange(n):
            yield iterable[int(round(r * i)):int(round(r * (i + 1)))]
    else:
        yield iterable


class ManagedTask(Task):
    abstract = True
    category = settings.JOB_DEFAULT_CATEGORY
    run_condition = True

    def apply(self, args=None, kwargs=None, link=None, link_error=None, **options):
        if not settings.CELERY_ENABLED:
            return
        return super(ManagedTask, self).apply(
            args=args, kwargs=kwargs, link=link, link_error=link_error, **options)

    def apply_async(self, args=None, kwargs=None, task_id=None, producer=None, link=None, link_error=None,
                    scheduled=False, countdown=settings.ASYNC_RACECOND_WAIT_SECS, **options):
        if not settings.CELERY_ENABLED:
            return
        return super(ManagedTask, self).apply_async(
            args, kwargs, task_id, producer, link, link_error,
            headers={'scheduled': scheduled, 'category': self.category},
            countdown=countdown, **options
        )

    def split__apply_async(self, iterable, args=None, kwargs=None, n_chunks=settings.CELERY_N_CHUNKS):
        if not args:
            args = []
        for chunk in _partition(iterable, n_chunks):
            self.apply_async(args=[chunk]+args, kwargs=kwargs)

    def __call__(self, *args, **kwargs):
        if kwargs.pop('_force_run', self.run_condition):
            with transaction_handler():
                return super(ManagedTask, self).__call__(*args, **kwargs)
        return 'Dry-Run due to condition'