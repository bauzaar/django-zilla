# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from contextlib import contextmanager
from fabric.context_managers import shell_env, cd, prefix
from fabric.state import env


@contextmanager
def activate_remote_env():
    with shell_env(BAUSTAGE=env.target_stage, DJANGO_SETTINGS_MODULE='baubackend.settings.%s' % env.target_stage), \
         cd('/srv/www/bauandrea/'), prefix('source /srv/env/bauandrea/bin/activate'):
        yield


@contextmanager
def ensure_target():
    from fabric_tasks.srv import target_prod
    if not getattr(env, 'target_stage', None):
        target_prod()
    yield


def get_ssh_command():
    return "ssh -p %s -i %s" % (env.port, env.key_filename)