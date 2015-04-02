# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from setuptools import setup, find_packages
from fabric.operations import local


git_short_hash = local('git rev-parse --short HEAD', capture=True)

setup(
    name='django-fishbone',
    version='0.5.dev%s' % git_short_hash,
    packages=find_packages(),
    url='https://github.com/silverfix/django-fishbone',
    license='BSD',
    author='Andrea Rabbaglietti',
    author_email = 'silverfix@gmail.com',
    description = 'A bunch of useful django apps',
    install_requires = [
        'django>=1.5',
        'celery',
        'fabric'
    ]
)