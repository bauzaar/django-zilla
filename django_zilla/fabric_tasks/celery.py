# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from fabric.decorators import task
from fabric.operations import local
from fabric.state import env


@task
def worker():
    """ Start celery worker """
    print local('celery worker -A %s -l INFO' % env.celery_app)


@task
def beat():
    """ Start celery beat """
    print local('celery beat -A %s -l INFO' % env.celery_app)


@task
def flush():
    """ Flush celery rabbitmq from target """
    print local('python manage.py celery_purge')