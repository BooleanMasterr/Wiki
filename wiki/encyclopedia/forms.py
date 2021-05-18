from django import forms
from . import util
from django.core.exceptions import ValidationError


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(), label="Title")
    content = forms.CharField(widget=forms.Textarea(), label="Markdown Content")

    def clean_title(self):
        title = self.cleaned_data.get("title")
        entries = [entry.lower() for entry in util.list_entries()]
        if title.lower() in entries:
            raise ValidationError("title already exists")
        return title


class Search(forms.Form):

    search = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search Encyclopedia",
            }
        )
    )


class UpdateForm(forms.Form):
    content = forms.CharField(label="Markdown Content", widget=forms.Textarea())
