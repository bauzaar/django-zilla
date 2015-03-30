# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from urlparse import urljoin
from django.conf import settings
from django.utils.encoding import force_text
from django_fishbone.utils.crypto import encrypt


def build_auto_login_url(url, cliente):
    param = 'auto_login=%s' % encrypt(cliente.email)
    return url + ('?' in url and '&%s' % param or '?%s' % param)


def build_full_url(url):
    return urljoin(settings.SITE_URL, force_text(url))