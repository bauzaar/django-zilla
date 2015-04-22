# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.core.management.base import BaseCommand
from django.core.cache import caches
from django.db import transaction
from django_fishbone.utils import redis_utils


class Command(BaseCommand):
    help = 'Flush cache'

    @transaction.atomic()
    def handle(self, *args, **options):
        cache_default = caches('default')
        cache_default.clear()
        redis_utils.reset_stats()
        self.stdout.write('Cleared cache.\n')