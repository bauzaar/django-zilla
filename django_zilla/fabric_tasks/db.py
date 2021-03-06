# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.conf import settings
from fabric.context_managers import hide, cd
from fabric.decorators import task
from fabric.operations import local, os, settings as fab_settings, run, sudo
from fabric.api import env
from django_zilla.fabric_tasks._utils import get_ssh_command, ensure_target


DB = settings.DATABASES['default']


@task
def dump(filepath='db.dump'):
    """ Issues pg_dump using proper django settings """
    return local('pg_dump --username=%s --host=%s -Fc %s > %s'
                 % (DB['USER'], DB['HOST'], DB['NAME'], filepath))


@task
def restore(filepath):
    """ Issues pg_restore using proper django settings """
    return local('pg_restore --username=%s --host=%s --dbname=%s %s'
                 % (DB['USER'], DB['HOST'], DB['NAME'], filepath))


@task
def exists():
    """ Check if DB exists """
    with fab_settings(hide('warnings'), warn_only=True):
        result = local('psql --username=%s --dbname=%s --host=%s --command="\q"'
                       % (DB['USER'], DB['NAME'], DB['HOST']))
    return result.succeeded


@task
def shell(user=DB['USER']):
    """ Open PostgreSQL shell using proper django settings """
    return local('psql --username=%s --dbname=postgres --host=%s' % (user, DB['HOST']))


@task
def psql_cmd(cmd, user=DB['USER']):
    """ Issues a command to psql using proper django settings """
    return local(
        'psql --username=%s --dbname=postgres --host=%s --command="%s"' % (user, DB['HOST'], cmd))


@task
def create():
    """ Create DB """
    if DB['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
        if exists():
            print "Cannot create DB %s: it exists already" % DB['NAME']
        else:
            print psql_cmd('CREATE DATABASE %s WITH ENCODING=\'UTF8\' CONNECTION LIMIT=-1' % DB['NAME'])
    else:
        print "Unknown DB Engine"


@task
def drop():
    """ Drop DB """
    if DB['ENGINE'] == 'django.db.backends.postgresql_psycopg2':
        if not exists():
            print "Cannot drop DB %s: it doesn't exist" % DB['NAME']
        else:
            print psql_cmd('drop database %s' % DB['NAME'])
    else:
        print "Unknown DB Engine"


@task
def dumpdata(filepath=getattr(settings, 'FIXTURE_PATH', '')):
    """ Dump initial_data.json by default DB """
    if os.path.isfile(filepath):
        os.remove(filepath)
    exclude_model_str = ' -e '.join(('south.migrationhistory', 'contenttypes', 'sessions', 'admin.logentry'))
    print local("python manage.py dumpdata --all -e %s --indent=4 > %s" % (exclude_model_str, filepath))


@task
def loaddata(filepath=getattr(settings, 'FIXTURE_PATH', '')):
    """ Load initial_data.json in default DB """
    if os.path.isfile(filepath):
        print local("python manage.py loaddata %s" % filepath)
    else:
        print "Nothing to load"


@task
def create_user():
    """ Create user """
    print psql_cmd("CREATE USER %s WITH PASSWORD '%s'" % (DB['USER'], DB['PASSWORD']), user='postgres')
    print psql_cmd("ALTER USER %s WITH SUPERUSER" % DB['USER'], user='postgres')


@task
def fetch():
    """ --> [REMOTE] Align DB/migrations/media from target """
    with ensure_target():
        from importlib import import_module
        settings_remote = import_module(name='%s.%s' % (settings.SETTINGS_PATH, env.target_stage))
        db_remote = settings_remote.DATABASES['default']

        media_dirname = os.path.split(settings.MEDIA_ROOT)[-1]
        print local('rsync --delete -azvvo '
                    '--exclude documenti ' # TODO
                    '--exclude documenti_store ' # TODO
                    '--exclude referenza_datafeed ' # TODO
                    '--exclude CACHE '
                    '-e "%s" %s:/srv/www/%s/%s/ %s/'
                    % (get_ssh_command(), env.host_string,
                       settings.PROJECT_NAME,
                       media_dirname, media_dirname))

        with cd('/srv/www/%s/' % settings.PROJECT_NAME):
            print run('pg_dump --username=%s --host=%s -Fc %s > temp.dump' \
                      % (db_remote['USER'], db_remote['HOST'], db_remote['NAME']))
            print local('scp -P %s -i %s -r -q %s:%s/temp.dump .' %
                        (env.port, env.key_filename, env.host_string, settings.PROJECT_NAME))
            print sudo('rm -f temp.dump')
            print drop()
            print create()
            print restore('temp.dump')
            print local('rm temp.dump')