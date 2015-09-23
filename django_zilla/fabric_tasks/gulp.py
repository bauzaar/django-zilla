# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from fabric.context_managers import hide, settings as fab_settings, lcd
from fabric.decorators import task
from fabric.operations import local
from fabric.api import env
from django.conf import settings
from django_zilla.fabric_tasks._utils import ensure_target
from django_zilla.fabric_tasks.git import get_current_branch


@task
def prod():
    """ --> [LOCAL] Compiles production frontend assets """
    local('gulp prod')


@task
def fetch():
    """ --> [LOCAL] Updates gulp-zilla's repository """
    lcd(settings.GULP_ZILLA_SRC_PATH)
    local('git pull')


@task
def update():
    """ --> [LOCAL] Updates gulp-zilla's repository """
    gulp_fetch()
    local('npm install')
