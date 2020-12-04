from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from ..models import Page


class PageView(DetailView):
    template_name = 'page_view.html'
    model = Page

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
