from datetime import datetime

from ..forms import PageEditForm
from ..models import Page
from ..views import PageView, PagesListView, UnknownPageView


# Entry points.
def display(request, slug=""):
    if not slug:
        return UnknownPageView.as_view()(request)
    
    return PageView.as_view()(request, slug=slug)

def create(request, slug=""):
    if doesSlugExist(slug):
        # If the page already exists, go to it.
        # TODO: Figure out how to incorporate a notification popup or something.
        return PageView.as_view()(request)

    created = Page.objects.get_or_create(
        slug=slug,
        defaults={
            'creator': request.user,
            'owner': request.user,
            'editing': request.user,
            'edit_lock': datetime.now(),
            'content': "<p>Welcome to your shiny new page!</p>"
        }
    )

    context = {
        'form': PageEditForm(instance=created)
    }

    return PageView.as_view()(request, pk=created.guid, extra_context=context)

def edit(request, slug=""):
    pass

def delete(request, slug=""):
    pass

# "Private" methods.
def hasEditLock(user, slug):
    pass

def doesSlugExist(slug):
    try:
        return bool(Page.objects.get(slug=slug))
    except Page.DoesNotExist:
        return False
