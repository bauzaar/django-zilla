# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from datetime import time, datetime
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import make_naive
import pytz


def make_aware_tz(dtime):
    return timezone.make_aware(dtime, timezone=pytz.timezone(settings.TIME_ZONE))


def get_utc_today():
    return timezone.now().date()


def get_local_today():
    return timezone.localtime(timezone.now()).date()


def get_utc_now():
    return timezone.now()


def get_local_now():
    return timezone.localtime(timezone.now())


def get_current_year():
    return get_local_now().year


def extract_datetime_range_from_request(request, from_datetime=None, to_datetime=None,
                                        param_name='timestamp_creazione', aware=True):
    if request.GET.get(param_name + '__gte'):
        from_datetime = datetime.strptime(request.GET[param_name + '__gte'], settings.DATE_FORMAT)
    else:
        from_datetime = settings.BAU_EPOCH_TIME

    if request.GET.get(param_name + '__lte'):
        to_datetime = datetime.strptime(request.GET[param_name + '__lte'], settings.DATE_FORMAT)
    else:
        to_datetime = datetime.now()

    if aware:
        from_datetime = make_aware_tz(from_datetime).replace(
            hour=time.min.hour, minute=time.min.minute, second=time.min.second, microsecond=time.min.microsecond)
        to_datetime = make_aware_tz(to_datetime).replace(
            hour=time.max.hour, minute=time.max.minute, second=time.max.second, microsecond=time.max.microsecond)

    return from_datetime, to_datetime


def extract_datetime_range_from_queryset(queryset, from_datetime=None, to_datetime=None, aware=True):
    if queryset.exists():
        if aware:
            from_datetime = timezone.localtime(queryset.order_by('timestamp_creazione')[0].timestamp_creazione)
            to_datetime = timezone.localtime(queryset.latest('timestamp_creazione').timestamp_creazione)
        else:
            from_datetime = make_naive(
                timezone.localtime(queryset.order_by('timestamp_creazione')[0].timestamp_creazione), timezone.utc)
            to_datetime = make_naive(
                timezone.localtime(queryset.latest('timestamp_creazione').timestamp_creazione), timezone.utc)
    return from_datetime, to_datetime