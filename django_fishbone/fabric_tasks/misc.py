# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from fabric.decorators import task
from fabric.operations import local, run
from fabric.state import env
from fabric_tasks._utils import activate_remote_env


@task
def flushsessions():
    """ Clear django client session """
    print local('python manage.py flushsessions')


@task
def flushcache():
    """ --> [REMOTE+LOCAL] Flush cache """
    if not hasattr(env, 'target_stage'):
        print local('python manage.py flushcache')
    else:
        with activate_remote_env():
            print run('python manage.py flushcache')


@task
def kindergarten():
    """ Execute python manage.py kindergarten """
    print local('python manage.py kindergarten')