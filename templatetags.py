from django_jinja import library
from jinja2 import contextfunction

from .forms import PageEditForm

import logging

logger = logging.getLogger(__name__)

@contextfunction
@library.global_function
def resolve_user(context):
    # logger.warn(dir(context['request'].user._wrapped))

    if context['request'].user._wrapped:
        return context['request'].user._wrapped.id

    return context['request'].user.id

@contextfunction
@library.global_function
def is_edited_by(context, user):
    editing = False

    if context.get('object'):
        editing = (context['object'].editing_id == user.id)
    
    return editing
