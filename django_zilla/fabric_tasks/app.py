# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from fabric.context_managers import hide, settings as fab_settings, lcd
from fabric.decorators import task
from fabric.operations import local
from django.conf import settings


@task
def run():
    """ --> [LOCAL] Starts django development server """
    local('python manage.py runserver')


@task
def shell():
    """ --> [LOCAL] Starts django shell """
    local('python manage.py shell')


@task
def dbshell():
    """ --> [LOCAL] Launches db shell through django """
    local('python manage.py dbshell')
