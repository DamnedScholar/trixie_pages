from django.views.generic import View, DetailView, ListView, CreateView, UpdateView

from .models import Page
from .forms import PageEditForm

default = {
    'title': 'New Page',
    'content': '<p>Start building here.</p>'
}

class PageView(UpdateView):
    template_name = 'page.html.jinja'
    model = Page
    form_class = PageEditForm

    def get_context_data(self, *args, **kwargs):
        self.object = self.get_object() or Page(default)

        return super().get_context_data(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object() or Page(default)
        self.initial = dict(self.object.__dict__)

        context = self.get_context_data(object=self.object)

        context.update({
            'initial': self.initial
        })
        return self.render_to_response(context)

class PagesListView(ListView):
    # TODO: Show a grid of pages with title, metadata, and thumbnails.
    template_name = 'list.html.jinja'
    model = Page

class UnknownPageView(View):
    # TODO: Display an error page and, if the user is logged in, an offer to create a new page. In a project with this as the primary pages app, this should replace the standard 404 page.
    template_name = '404.html.jinja'

class CreatePageView(CreateView):
    model = Page
    fields = '__all__'
    template_name = 'page.html.jinja'
    form_class = PageEditForm

    def get_context_data(self, **kwargs):
        self.object = self.get_object() or Page(default)
        self.initial = self.object.__dict__

        return super().get_context_data(**kwargs)

class UpdatePageView(UpdateView):
    model = Page
    template_name = 'page.html.jinja'
    form_class = PageEditForm

    def get_context_data(self, **kwargs):
        self.object = self.get_object() or Page(default)
        self.initial = self.object.__dict__

        return super().get_context_data(**kwargs)
