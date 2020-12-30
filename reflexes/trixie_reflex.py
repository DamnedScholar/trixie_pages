from sockpuppet.reflex import Reflex


class TrixieReflex(Reflex):
    def toggle_edit_mode(self):
        # Check if the current model has an edit lock. If the user passes or the model is free, set an edit lock and refresh the page.
        pass

    def create_page(self):
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

    def remember_view_event(self):
        pass
