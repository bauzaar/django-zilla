# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.db import transaction


class Command(BaseCommand):
    help = 'Clean-up ContentType DB Model'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        for c in ContentType.objects.all():
            if not c.model_class():
                self.stdout.write("Deleting [%s]\n" % c)
                confirm = raw_input("Are you sure? Type 'yes' to continue: ")
                if confirm == 'yes':
                    c.delete()
        self.stdout.write('\nFinished.')