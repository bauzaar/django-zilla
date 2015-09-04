# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from setuptools import setup, find_packages
import subprocess
import shlex


GIT_HEAD_REV = subprocess.check_output(shlex.split('git rev-parse --short HEAD')).strip()

setup(
    name='django-zilla',
    version='0.5.dev#%s' % GIT_HEAD_REV,
    packages=find_packages(),
    url='https://github.com/bauzaar/django-zilla',
    license='BSD',
    author='Andrea Rabbaglietti',
    author_email = 'silverfix@gmail.com',
    description = 'A bunch of useful django apps',
    install_requires = [
        'django>=1.8',
    ]
)
