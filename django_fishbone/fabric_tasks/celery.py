# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from fabric.decorators import task
from fabric.operations import local


@task
def worker():
    """ Start celery worker """
    print local('celery worker -A django_fishbone.celery_manager -l INFO')


@task
def beat():
    """ Start celery beat """
    print local('celery beat -A django_fishbone.celery_manager -l INFO')


@task
def flush():
    """ Flush celery rabbitmq from target """
    print local('python manage.py celery_purge')