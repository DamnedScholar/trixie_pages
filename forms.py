from django import forms

from .models import Page

class PageEditForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'slug']

class SlugForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['slug']
