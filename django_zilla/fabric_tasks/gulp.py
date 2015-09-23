# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from fabric.context_managers import hide, settings as fab_settings, lcd
from fabric.decorators import task
from fabric.operations import local
from django.conf import settings


@task
def prod():
    """ --> [LOCAL] Compiles production frontend assets """
    local('gulp prod')


@task
def fetch():
    """ --> [LOCAL] Updates gulp-zilla's repository """
    with lcd(settings.GULP_ZILLA_SRC_PATH):
        local('git pull')


@task
def update():
    """ --> [LOCAL] Installs or updates gulp-zilla's dependencies """
    local('gulp install')
