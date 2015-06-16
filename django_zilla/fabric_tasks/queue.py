# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from celery.app import app_or_default
from celery.bin.worker import worker as Worker
from celery.bin.beat import beat as Beat
from fabric.decorators import task


@task
def worker():
    """ Start celery worker """
    w = Worker(app_or_default())
    options = {
        'loglevel': 'INFO',
        'traceback': True
    }
    w.run(**options)


@task
def beat():
    """ Start celery beat """
    b = Beat(app_or_default())
    options = {
        'loglevel': 'INFO',
        'traceback': True
    }
    b.run(**options)


@task
def flush():
    """ Flush celery rabbitmq from target """
    n = app_or_default().control.purge()
    print '%d message(s) purged.\n' % n