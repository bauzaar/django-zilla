# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from django import template
from django.forms.forms import BoundField
from django.forms.util import flatatt
from django_zilla.form_layout.render import render_block_to_string


register = template.Library()


@register.simple_tag
def field(field, field_type, *args, **kwargs):
    if not isinstance(field, BoundField):
        return ''

    d = {
        'id': field.auto_id,
        'css_classes': field.css_classes,
        'errors': field.errors,
        'help_text': field.help_text,
        'html_name': field.html_name,
        'id_for_label': field.id_for_label,
        'is_hidden': field.is_hidden,
        'label': field.label,
        'label_tag': field.label_tag,
        'name': field.name,
        'value': field.value,
        'widget_attrs': flatatt(field.field.widget.attrs),
        'required': field.field.required
    }

    if hasattr(field.field, 'choices'):
        d['choices'] = field.field.choices

    d.update(kwargs)

    return render_block_to_string(
        'form_layout/fields.html', field_type, d)


@register.simple_tag
def form_helper(helper_type, *args, **kwargs):
      return render_block_to_string(
        'form_layout/form_helpers.html', helper_type)