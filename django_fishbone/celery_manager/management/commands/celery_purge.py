# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from celery.app import app_or_default
from django.core.management.base import BaseCommand
from django.db import transaction
from django_fishbone.celery_manager import app


class Command(BaseCommand):
    help = 'Purge task queue'

    @transaction.atomic()
    def handle(self, *args, **options):
        n = app_or_default.control.purge()
        self.stdout.write('%d message(s) purged.\n' % n)