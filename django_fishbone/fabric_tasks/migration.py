# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.conf import settings
from fabric.decorators import task
from fabric.operations import local
from django_fishbone.utils import legacy_layer


@task
def makemigrations():
    """ Makes migrations """
    return legacy_layer.makemigrations()


@task
def migrate():
    """ Applies migrations """
    for app_label in settings.APPS_TO_MIGRATE:
        print local('python manage.py migrate %s' % app_label)