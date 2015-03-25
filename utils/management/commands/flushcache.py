# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.core.management.base import BaseCommand
from django.db import transaction
from django.core import cache
from utils import redis_utils


class Command(BaseCommand):
    help = 'Flush cache'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        cache_default = cache.get_cache('default')
        cache_default.clear()
        redis_utils.reset_stats()
        self.stdout.write('Cleared cache.\n')