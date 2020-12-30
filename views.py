from django.shortcuts import render
from django.views.generic import View, DetailView, ListView
from django.views.generic.base import TemplateView
from .models import Page


class PageView(DetailView):
    template_name = 'page.html'
    model = Page

class PagesListView(ListView):
    # TODO: Show a grid of pages with title, metadata, and thumbnails.
    template_name = 'list.html'
    model = Page

class UnknownPageView(View):
    # TODO: Display an error page and, if the user is logged in, an offer to create a new page. In a project with this as the primary pages app, this should replace the standard 404 page.
    template_name = '404.html'
