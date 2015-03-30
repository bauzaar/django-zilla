# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from setuptools import setup, find_packages


setup(
    name='django-fishbone',
    version='0.1',
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