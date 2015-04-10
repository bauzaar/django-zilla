# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from fabric.decorators import task
from fabric.operations import local, settings as fab_settings
from fabric.context_managers import hide


@task
def makemigrations():
    """ Makes migrations """
    with fab_settings(hide('warnings'), warn_only=True):
        print local('python manage.py makemigrations')


@task
def migrate():
    """ Applies migrations """
    with fab_settings(hide('warnings'), warn_only=True):
        print local('python manage.py migrate')