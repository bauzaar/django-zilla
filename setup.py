# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from setuptools import setup, find_packages
import subprocess


git_short_hash = subprocess.check_output(["git rev-parse --short HEAD"])

setup(
    name='django-fishbone',
    version=git_short_hash,
    packages=find_packages(),
    url='https://github.com/silverfix/django-fishbone',
    license='BSD',
    author='Andrea Rabbaglietti',
    author_email = 'silverfix@gmail.com',
    description = 'A bunch of useful django apps',
    install_requires = [
        'django>=1.5',
        'celery'
    ]
)