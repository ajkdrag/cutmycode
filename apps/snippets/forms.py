from django import forms
from django.forms import Textarea
from .models import Snippet


class SnippetCreateForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ["title", "code", "description", "language"]
        widgets = {
            "description": Textarea(attrs={"rows": 2}),
        }
