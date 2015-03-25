# -*- coding: utf-8 -*-

from django.db.models import Manager
from django.db.models.query import QuerySet


class OnlineManager(Manager):
    class OnlineCustomQuerySet(QuerySet):
        def online(self, online=True):
            return self.filter(online=online)

    def get_query_set(self):
        return OnlineManager.OnlineCustomQuerySet(self.model)

    def online(self, *args, **kwargs):
        return self.get_query_set().online(*args, **kwargs)