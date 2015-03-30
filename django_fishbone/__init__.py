  # -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
import django
from django.db import transaction


if django.VERSION[0] == 1 and django.VERSION[1] >= 6:
    transaction_handler = transaction.atomic
else:
    transaction_handler = transaction.commit_on_success
