from django import forms
from src.domain.constants import Language


class SnippetCreationForm(forms.Form):
    title = forms.CharField(max_length=120)
    code = forms.CharField(widget=forms.Textarea(attrs={"rows": 6}))
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    language = forms.ChoiceField(choices=Language.choices())
