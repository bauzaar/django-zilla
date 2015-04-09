  # -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import django
from django.db import transaction
from django.conf import settings
from fabric.operations import local


if django.VERSION[0] > 1 or (django.VERSION[0] == 1 and django.VERSION[1] >= 6):
    transaction_handler = transaction.atomic
else:
    transaction_handler = transaction.commit_on_success


if django.VERSION[0] > 1 or (django.VERSION[0] == 1 and django.VERSION[1] >= 8):
    def makemigrations():
        print local('python manage.py makemigrations')
else:
    def makemigrations():
        for app_label in settings.APPS_TO_MIGRATE:
            print local('python manage.py schemamigration %s --auto' % app_label)