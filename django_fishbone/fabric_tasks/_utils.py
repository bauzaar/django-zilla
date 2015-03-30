# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from contextlib import contextmanager
from fabric.state import env


@contextmanager
def ensure_target():
    from django_fishbone.fabric_tasks.srv import target_prod
    if not getattr(env, 'target_stage', None):
        target_prod()
    yield


def get_ssh_command():
    return "ssh -p %s -i %s" % (env.port, env.key_filename)