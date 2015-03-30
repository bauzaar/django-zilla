# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from celery import states
from django.conf import settings
from django.db.models import CharField, TextField, BooleanField, DateTimeField, Model
from django_fishbone.utils.datetime_utils import get_utc_now


class Job(Model):
    state = CharField(max_length=10, default=states.PENDING)
    task = CharField(max_length=256, db_index=True)
    task_id = CharField(max_length=36, unique=True, db_index=True)
    category = CharField(max_length=15, default=settings.JOB_DEFAULT_CATEGORY,
                         choices=settings.JOB_CATEGORY_CHOICES.items())
    args = TextField(blank=True)
    kwargs = TextField(blank=True)
    result = TextField(blank=True)
    scheduled = BooleanField(default=False)
    timestamp_created = DateTimeField(default=get_utc_now, auto_now_add=True, db_index=True, editable=False)
    timestamp_modified = DateTimeField(default=get_utc_now, auto_now=True, db_index=True, editable=False)
    timestamp_prerun = DateTimeField(editable=False, null=True, blank=True)
    timestamp_postrun = DateTimeField(editable=False, null=True, blank=True)

    def elapsed_time(self):
        if not self.timestamp_prerun or not self.timestamp_postrun:
            return 'N/a'
        secs = (self.timestamp_postrun - self.timestamp_prerun).total_seconds()
        if secs < 60:
            return '%.1f sec(s)' % secs
        return '%d min(s), %.1f sec(s)' % (secs // 60, secs % 60)

    def __unicode__(self):
        return self.task