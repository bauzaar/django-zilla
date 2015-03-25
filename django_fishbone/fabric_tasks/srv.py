# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from fabric.context_managers import hide, settings as fab_settings
from fabric.decorators import task
from fabric.operations import local
from fabric.api import env
from fabric_tasks._utils import ensure_target
from fabric_tasks.git import get_current_branch


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
    DIST_FILEPATH = 'baufrontend/static_src/_dist/'
    with ensure_target():
        local("git add --all .")
        local("git add -f %s" % DIST_FILEPATH)
        with fab_settings(hide('warnings'), warn_only=True):
            local("git commit -m 'deploy bauandrea/%s'" % env.target_stage)
        local("git rm -r --cached %s" % DIST_FILEPATH)
        local("git push %s %s -f" % (env.target_stage, get_current_branch()))
        local("git commit --amend -a --no-edit --allow-empty")