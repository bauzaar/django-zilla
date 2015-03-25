# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from setuptools import setup


setup(
    name='django-fishbone',
    version='1.0',
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