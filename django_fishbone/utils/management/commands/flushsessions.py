# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.core.management.base import BaseCommand
from django.core import cache
from django.db import transaction
from django_fishbone.utils import redis_utils


class Command(BaseCommand):
    help = 'Flush sessions'

    @transaction.atomic()
    def handle(self, *args, **options):
        cache_session_bucket = cache.get_cache('session_bucket')
        cache_session_bucket.clear()
        redis_utils.reset_stats()
        self.stdout.write('Cleared cache.\n')