# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.core.management.base import BaseCommand
from django_fishbone.utils.legacy_layer import transaction_handler
from django_fishbone.celery_manager import app


class Command(BaseCommand):
    help = 'Purge task queue'

    @transaction_handler()
    def handle(self, *args, **options):
        n = app.control.purge()
        self.stdout.write('%d message(s) purged.\n' % n)