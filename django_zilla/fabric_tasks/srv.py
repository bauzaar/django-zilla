# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from fabric.context_managers import hide, settings as fab_settings
from fabric.decorators import task
from fabric.operations import local
from fabric.api import env
from django.conf import settings
from django_zilla.fabric_tasks._utils import ensure_target
from django_zilla.fabric_tasks.git import get_current_branch


@task
def target_test():
    """ Set host target to 'test' """
    env.host_string = 'www-data@5.196.1.64'
    env.target_stage = 'test'
    env.port = '4444'


@task
def target_prod():
    """ Set host target to 'prod' [DEFAULT] """
    env.host_string = 'www-data@37.59.25.139'
    env.target_stage = 'prod'
    env.port = '4444'


@task
def deploy():
    """ --> [REMOTE] Deploy to target env """
    with ensure_target():
        # Avoid pushing dumps & other rubbish.
        # Only push up to the last explicit commit
        # local("git add --all .")
        local("git add -f %s" % settings.STATIC_DIST_FILEPATH)
        with fab_settings(hide('warnings'), warn_only=True):
            local("git commit -m 'deploy %s/%s'" % (settings.PROJECT_NAME, env.target_stage))
            local("git rm -r --cached %s" % settings.STATIC_DIST_FILEPATH)
        local("git push %s %s -f" % (env.target_stage, get_current_branch()))
        local("git commit --amend -a --no-edit --allow-empty")