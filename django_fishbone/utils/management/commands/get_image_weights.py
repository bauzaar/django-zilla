# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import os
import traceback
from celery.utils.debug import humanbytes
from django.core.management.base import BaseCommand
from django.db import transaction
from baubackend.apps.erp.models import Referenza


class Command(BaseCommand):
    help = 'Get comma-separated image-weights'

    @transaction.commit_on_success
    def handle(self, limit=None, *args, **options):
        try:
            for r in Referenza.objects.all():
                weight = int(humanbytes(os.path.getsize(r.get_immagine().path.replace('kB', '').split('.')[0])))
                print "%s,%s" % (r.codice, weight)
        except:
            traceback.print_exc()
        finally:
            self.stdout.write('\nFinished.')