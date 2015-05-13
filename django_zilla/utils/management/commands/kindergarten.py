# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import traceback
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Generic command for various stuff'

    @transaction.atomic
    def handle(self, limit=None, *args, **options):
        try:
            pass
            # WRITE DOWN HERE

            # END WRITE
        except:
            traceback.print_exc()
        finally:
            self.stdout.write('\nFinished.')