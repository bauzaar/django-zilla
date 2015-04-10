# -*- coding: utf-8 -*-

from __future__ import unicode_literals, division
from copy import copy
from django.template.loader_tags import BlockNode
from django.template import loader, Context


def render_block_to_string(template_name, block_name, d=None, context_instance=None):
    d = d or {}
    if context_instance:
        context_instance.update(d)
    else:
        context_instance = Context(d)

    to_visit = copy(loader.get_template(template_name).template.nodelist)
    while to_visit:
        current_node = to_visit.pop()
        if isinstance(current_node, BlockNode) and current_node.name == block_name:
            return current_node.render(context_instance)
        else:
            if hasattr(current_node, 'nodelist'):
                to_visit.extend(current_node.nodelist)

    raise RuntimeError('Block "%s" not found' % block_name)