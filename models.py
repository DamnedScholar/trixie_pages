from uuid import uuid4

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields

from django_hashids import HashidsField

from .widgets import TrixieWidget


class TrixieField(fields.TextField):
    def formfield(self, **kwargs):
        trixie = { 'widget': TrixieWidget }
        return super().formfield(**trixie)

class BasePage(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    # HashidsField requires salt if there's none in `settings.py`.
    hashid = HashidsField(real_field_name=guid, salt="Itsy bitsy spider")
    title = models.CharField(max_length=500, blank=True)
    slug = models.SlugField()
    content = TrixieField()
    syndicate = models.BooleanField(default=False)
    template = models.CharField(max_length=50, blank=True)
    editing = models.UUIDField(blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="page_creator"
        null=True, on_delete=models.SET_NULL)
    creator_username = models.CharField(max_length=50, null=True)
    owner = models.ForeignKey(User, related_name="page_owner"
        null=True, on_delete=models.SET_NULL)
    owner_username = models.CharField(max_length=50, null=True)
    # TODO: I need to implement tagging and metadata somehow.
    # tags = TagField(blank=True)
    # meta = models.OneToOneField(MetaTags, null=True, on_delete=models.SET_NULL)
