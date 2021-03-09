from django_jinja import library
from jinja2 import contextfunction

from .forms import PageEditForm


@contextfunction
@library.global_function
def is_edited_by(context, user):
    editing = False

    if context.get('object'):
        editing = (context['object'].editing_id == user.id)
    
    return editing
