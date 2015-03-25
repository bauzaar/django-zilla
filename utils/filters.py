# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter, FieldListFilter
from django.contrib.admin.widgets import AdminDateWidget
from django.db import models
from datetime import datetime
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from utils.datetime_utils import make_aware_tz
from django.utils.translation import ugettext as _


class CategoriaFilter(SimpleListFilter):
    title = "Categoria"
    parameter_name = 'categoria'

    def lookups(self, request, model_admin):
        from baubackend.apps.erp.models import Categoria
        return [(categoria.id, mark_safe(("&nbsp;&nbsp;&nbsp;" * categoria.get_level()) + categoria.nome))
                for categoria in Categoria.objects.all()]


class DateRangeFilter(FieldListFilter):
    class DateRangeForm(forms.Form):
        def __init__(self, *args, **kwargs):
            field_name = kwargs.pop('field_name')
            super(DateRangeFilter.DateRangeForm, self).__init__(*args, **kwargs)

            self.fields['%s__gte' % field_name] = \
                forms.DateField(label='Da', widget=AdminDateWidget(
                    attrs={'placeholder': 'gg/mm/aaaa', 'style': 'width: 85px'}),
                                localize=True,
                                required=False)

            self.fields['%s__lte' % field_name] = \
                forms.DateField(label='A', widget=AdminDateWidget(
                    attrs={'placeholder': 'gg/mm/aaaa', 'style': 'width: 85px'}),
                                localize=True,
                                required=False)

    template = 'admin/custom_fragments/daterange_filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_upto = '%s__lte' % field_path
        super(DateRangeFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        return []

    def expected_parameters(self):
        return self.lookup_kwarg_since, self.lookup_kwarg_upto

    def get_form(self, request):
        return self.DateRangeForm(data=self.used_parameters, field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            filter_params = {}
            for k, v in self.form.cleaned_data.iteritems():
                if not v:
                    continue

                if '__lte' in k:
                    combining_time = datetime.max.time()
                elif '__gte' in k:
                    combining_time = datetime.min.time()
                else:
                    continue

                datetime_aware = make_aware_tz(datetime.combine(v, combining_time))

                filter_params[k] = datetime_aware

            return queryset.filter(**filter_params)

        else:
            return queryset

admin.FieldListFilter.register(lambda f: isinstance(f, models.DateField), DateRangeFilter)


class DefaultListFilter(SimpleListFilter):
    all_value = '_all'

    def default_value(self):
        raise NotImplementedError()

    def queryset(self, request, queryset):
        if self.parameter_name in request.GET and request.GET[self.parameter_name] == self.all_value:
            return queryset

        if self.parameter_name in request.GET:
            return queryset.filter(**{self.parameter_name: request.GET[self.parameter_name]})

        return queryset.filter(**{self.parameter_name: self.default_value()})

    def choices(self, cl):
        yield {
            'selected': self.value() == self.all_value,
            'query_string': cl.get_query_string({self.parameter_name: self.all_value}, []),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup) or (
                    self.value() is None and force_text(self.default_value()) == force_text(lookup)),
                'query_string': cl.get_query_string({self.parameter_name: lookup}, []),
                'display': title,
            }