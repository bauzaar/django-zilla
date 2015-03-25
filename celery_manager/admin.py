# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.contrib.admin import ModelAdmin, site
from celery_manager.models import Job
from utils.admin_mixin import NotAddableMixin


class JobAdmin(NotAddableMixin, ModelAdmin):
    list_display = ('task', 'scheduled', 'category',
                    'state', 'elapsed_time', 'timestamp_creazione')
    list_filter = ('state', 'category', 'scheduled', 'task')
    search_fields = ('task', 'args', 'kwargs', 'result')
    readonly_fields = ('timestamp_creazione', 'timestamp_modifica')
    fields = ('state', 'task', 'task_id', 'category', 'args', 'kwargs', 'result', 'scheduled',
              'timestamp_creazione', 'timestamp_modifica')


site.register(Job, JobAdmin)