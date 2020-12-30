from django.conf.urls import url
from .controllers import page

urlpatterns = [
    url(r'^<slug:page_slug>/$', page.display, name="trixie-page"),
    url(r'^new/<slug:page_slug>/$', page.create, name="trixie-create"),
    url(r'^edit/<slug:page_slug>/$', page.edit, name="trixie-edit"),
    url(r'^delete/<slug:page_slug>/$', page.delete, name="trixie-delete"),
]
