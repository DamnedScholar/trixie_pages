import asyncio
import json

from django.contrib.auth.models import User

from django_jinja.backend import Jinja2
from sockpuppet.channel import Channel
from sockpuppet.reflex import Reflex

from ..models import Page
from ..forms import PageEditForm, SlugForm

from lib.puppet_show.patches.reflex import UserFixedReflex

import logging

logger = logging.getLogger(__name__)


class TrixieReflex(UserFixedReflex):
    trixie = {
        "modal": "",  # HTML string rendered inside the page for dialogs
    }

    # TODO: Seriously consider replacing Trix with Quill. Figure out a non-Trix-related name for this module. I feel like I know which editor gives me what I want.

    def edit_mode(self):
        """
        Enable editing of the page.
        """
        # TODO: Look into CSRF protection for this function. It's probably not supported in the framework, but Channels might have a solution. I might be able to roll my own, too, and build a helper into Sockpuppet to make it so that you can't trigger a specific Reflex without a CSRF token (like a decorator function that checks `self.params`).
        self.object = Page.objects.filter(slug=self.element.dataset["slug"])[0]

        user = self.request.user

        if self.object.request_edit_lock_for_user(user):
            # Check if the current model has an edit lock. If the user passes
            # or the model is free, set an edit lock and refresh the page.
            self.form = PageEditForm(self.object.__dict__)

    def view_mode(self):
        """
        Turn off edit mode and switch to read-only.
        """
        obj = Page.objects.filter(slug=self.element.dataset["slug"])[0]

        form = PageEditForm(self.params)

        if form.is_valid():
            for attr, value in form.cleaned_data.items():
                setattr(obj, attr, value)

        # This also saves.
        obj.clear_edit_lock()

    def create_page(self):
        """
        Pop up a modal to take a slug as input.
        """
        channel = self.open_channel()

        opts = {
            "label": "Please type a slug for the new page that hasn't been used yet.",
            "form": SlugForm(),
            "action": "trixie#create_confirm",
        }

        output = Jinja2.get_template(Jinja2,
            template_name="widgets/slugform.html.jinja"
        ).render(opts, self.request)

        channel.dispatch_event(
            {
                "name": "slug-prompt",
                "detail": output,
                "selector": "document"
            }
        )

        channel.inner_html(
            {
                "selector": "#modal",
                "html": output,
                "focus_selector": "input"
            }
        )

        channel.broadcast()

    def create_confirm(self):
        # Check that the chosen slug is valid and unclaimed.
        pass

    def copy_page(self):
        pass

    def delete_page(self):
        # Check for an edit lock, then throw up a modal to confirm the deletion.
        pass

    def confirm_delete(self):
        # Check for an edit lock once more (just in case), and then delete.
        pass

    def show_metrics(self):
        pass

    def retain_view_event(self):
        pass

    # TODO: Prototype convenience functions for interfacing with CableReady operations and making declarative broadcasts. The default behavior takes all Reflex instance variables, plugs them into the context, and rerenders the view function based on the changed state, which doesn't accommodate for rendering arbitrary templates for components like modals.

    def open_channel(self):
        '''
        Return a Channel object on which we can perform CR operations.
        '''
        return Channel(self.get_channel_id())
