# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.contrib.contenttypes.models import ContentType
from django.core import cache
from fabric.decorators import task
from fabric.operations import local


@task
def flushsessions():
    """ Clear django client session """
    print local('python manage.py flushsessions')


@task
def flushcache():
    """ Flush cache """
    print local('python manage.py flushcache')


@task
def kindergarten():
    """ Execute python manage.py kindergarten """
    print local('python manage.py kindergarten')


@task
def clean_contenttypes():
    """ Clean django ContentType model """
    for c in ContentType.objects.all():
        if not c.model_class():
            print "Deleting [%s]\n" % c
            confirm = raw_input("Are you sure? Type 'yes' to continue: ")
            if confirm == 'yes':
                c.delete()
    print 'Finished.'


@task
def flush_cache():
    """ Flush django default cache """
    from django_zilla.utils import redis_utils
    cache_default = cache.get_cache('default')
    cache_default.clear()
    redis_utils.reset_stats()
    print 'Cache flushed.'


@task
def clear_sessions():
    """ Clear django sessions """
    from django_zilla.utils import redis_utils
    cache_session = cache.get_cache('session_bucket')
    cache_session.clear()
    redis_utils.reset_stats()
    print 'Sessions cleared.'