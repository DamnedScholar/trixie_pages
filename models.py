from uuid import uuid4

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields

import arrow
from django_hashids import HashidsField

from .widgets import TrixieWidget


class TrixieField(fields.TextField):
    def formfield(self, **kwargs):
        trixie = { 'widget': TrixieWidget }
        return super().formfield(**trixie)

class BasePage(models.Model):
    guid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(unique=True)
    content = TrixieField(blank=True)
    template = models.CharField(max_length=50, blank=True)
    editing = models.ForeignKey(User, related_name="page_edit_lock",
        blank=True, null=True, on_delete=models.SET_NULL)
    edit_lock = models.DateTimeField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, related_name="page_creator",
        null=True, on_delete=models.SET_NULL)
    creator_username = models.CharField(max_length=50, null=True)
    owner = models.ForeignKey(User, related_name="page_owner",
        null=True, on_delete=models.SET_NULL)
    owner_username = models.CharField(max_length=50, null=True)

    published = models.BooleanField(default=False)
    # TODO: Look into delayed publication.
    # TODO: I need to implement tagging and metadata somehow.
    # tags = TagField(blank=True)
    # meta = models.OneToOneField(MetaTags, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'/{ self.slug } ({ self.guid })'

    def get_absolute_url(self):
        return f'/{ self.slug }'

    def can_be_edited_by(self, user, now):
        if self.editing == user:
            return True

        if (not self.editing):
            return True
            
        try:
            # An exception here means that there's not a valid value on the edit lock and we should ignore it.
            meantime = now - self.edit_lock
            if (meantime.seconds > 7264):
                return True
        except TypeError:
            return False

        return False

    def reward_edit_lock(self, user, now):
        self.editing = user
        self.edit_lock = str(now)

        self.save()

    def clear_edit_lock(self):
        self.editing = None
        self.edit_lock = None

        self.save()

    def request_edit_lock_for_user(self, user):
        now = arrow.now(tz='CST')

        if self.can_be_edited_by(user, now):
            self.reward_edit_lock(user, now)
            
        return (self.editing == user)

class Page (BasePage):
    pass
