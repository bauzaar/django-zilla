# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
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