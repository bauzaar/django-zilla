# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.core.management.base import BaseCommand
from django.db import transaction
from celery_manager import app

class Command(BaseCommand):
    help = 'Purge task queue'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        n = app.control.purge()
        self.stdout.write('%d message(s) purged.\n' % n)