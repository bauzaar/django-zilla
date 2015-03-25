# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import os
from django.conf import settings
from fabric.context_managers import hide
from fabric.decorators import task
from fabric.operations import local, settings as fab_settings
from fabric.utils import abort


def _rm_last_migration(app):
    l = []
    migration_app_dir = os.path.join(settings.MIGRATIONS_DIR, app)
    for filename in os.listdir(migration_app_dir):
        filepath = os.path.join(migration_app_dir, filename)
        l.append((os.path.getmtime(filepath), filepath))

    l.sort(key=lambda t: t[0], reverse=True)
    os.remove(l[0][1])
    os.remove(l[1][1])


@task
def reset():
    """ Reset and init migrations files """
    for root, dirs, filenames in os.walk(settings.MIGRATIONS_DIR):
        for filename in filenames:
            if filename == '__init__.py':
                continue
            filepath = os.path.join(root, filename)
            os.remove(filepath)

    for app in settings.APPS_TO_MIGRATE:
        print local("python manage.py schemamigration %s --initial" % app)


@task
def migrate():
    """ schemamigration --auto && migrate """
    for app in settings.APPS_TO_MIGRATE:
        with fab_settings(hide('warnings'), warn_only=True):
            schema_result = local("python manage.py schemamigration %s --auto" % app)
        if schema_result.succeeded:
            print schema_result
            with fab_settings(hide('warnings'), warn_only=True):
                migrate_result = local("python manage.py migrate %s" % app)
            if migrate_result.succeeded:
                print migrate_result
            else:
                _rm_last_migration(app)
                abort(migrate_result)
