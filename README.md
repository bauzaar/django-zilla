# django-fishbone
A bunch of useful django apps!

## Supported django version
django >= 1.5

## Settings required (settings.py)
PROJECT_NAME (e.g. 'bauandrea')
STATIC_DIST_FILEPATH (e.g. 'baufrontend/static_src/_dist/')
PROJECT_EPOCH_TIME (e.g. datetime.strptime('13/12/2012', DATE_FORMAT))
SETTINGS_PATH (e.g. 'baubackend.settings')

## Quick Start

Do you need to create a fabfile.py into your project root folder

```python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django.conf import settings
from fabric.api import env
from fabric.contrib import django as fab_django
from fabric.decorators import task
from fabric.operations import local, os
from baubackend.settings import DJANGO_SETTINGS_MODULE, STAGE


if STAGE == 'dev':
    env.key_filename = r"C:\cygwin\home\SilverFix\.ssh\id_rsa_BAUZAAR"
elif STAGE == 'test':
    env.key_filename = r"/root/.ssh/id_rsa"
elif STAGE == 'dev_kreo':
    env.key_filename = r"/Users/mac/.ssh/id_rsa"

fab_django.settings_module(DJANGO_SETTINGS_MODULE)


@task
def shell():
    """ Open a django shell through IPython """
    print local("python %s shell" % os.path.join(settings.PROJECT_ROOT, 'manage.py'))


from django_fishbone.fabric_tasks import celery, db, migration, misc, srv, git
```