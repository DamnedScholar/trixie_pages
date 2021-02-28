from django.urls import path

from .views import PageView, CreatePageView, UpdatePageView

urlpatterns = [
    path(r'', PageView.as_view(), { 'slug': 'ruthies' }, name="home"),
    path(r'<slug:slug>', PageView.as_view(), name="trixie-page"),
    path(r'new/<slug:slug>', CreatePageView.as_view(), name="trixie-create"),
    path(r'edit/<slug:slug>', UpdatePageView.as_view(), name="trixie-edit"),
    # TODO: Consider possible delete endpoint.
    # url(r'^/delete/<slug:slug>', DeletePageView.as_view(), name="trixie-delete"),
]
