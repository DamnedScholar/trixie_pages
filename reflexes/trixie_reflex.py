import json

from django_jinja.backend import Jinja2
from sockpuppet.channel import Channel
from sockpuppet.reflex import Reflex

from ..models import Page
from ..forms import PageEditForm, SlugForm


class TrixieReflex(Reflex):
    trixie = {
        'modal': '',    # HTML string rendered inside the page for dialogs
    }

    # TODO: Seriously consider replacing Trix with Quill. Figure out a non-Trix-related name for this module. I feel like I know which editor gives me what I want.

    def edit_mode(self):
        # raise AttributeError(self.element.dataset['slug'])
        self.object = Page.objects.filter(slug=self.element.dataset['slug'])[0]

        if self.object.request_edit_lock_for_user(self.request.user):
            # Check if the current model has an edit lock. If the user passes
            # or the model is free, set an edit lock and refresh the page.
            self.form = PageEditForm(self.object.__dict__)

    def view_mode(self):
        obj = Page.objects.filter(slug=self.element.dataset['slug'])[0]

        form = PageEditForm(self.params)

        if form.is_valid():
            for attr, value in form.cleaned_data.items(): 
                setattr(obj, attr, value)

        # This also saves.
        obj.clear_edit_lock()

    def create_page(self):
        # Pop up a modal to take a slug as input.
        channel = self.open_channel()

        template = Jinja2.get_template('widgets/slugform.html.jinja')

        output = template.render({
            'label': 'Please type a slug for the new page that hasn\'t been used yet.',
            'form': SlugForm(),
            'reflex': self.__name__ + '#create_confirm'
        }, self.request)

        # channel.inner_html({
        #     'selector': '#reflex_modal',
        #     'focus-selector': 'input',
        #     'html': output
        # })

        # payload = {
        #     'label': 'Please type a slug for the new page',
        #     'helpText': 'Slug must not be used yet.',
        # }

        channel.dispatch_event({
            'name': 'slug-prompt',
            'detail': output,
            'selector': 'document',
        })

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
        # Return a Channel object on which we can perform CR operations.
        return Channel(self.get_channel_id())
