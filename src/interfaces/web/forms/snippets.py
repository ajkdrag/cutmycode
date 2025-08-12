from django import forms
from src.domain.constants import Language


class SnippetCreationForm(forms.Form):
    title = forms.CharField(
        max_length=120,
        widget=forms.TextInput(
            attrs={
                "placeholder": "In-place quick sort ...",
                "class": "c-input",
            }
        ),
    )
    code = forms.CharField(
        # widget isn't used when CodeMirror is active
        # CodeMirror creates a div and makes textarea hidden
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "class": "c-textarea",
                "x-ref": "editor",
            }
        ),
        initial="# Your code here\n",
    )
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "class": "c-textarea",
            }
        ),
    )
    language = forms.ChoiceField(
        choices=Language.choices(),
        widget=forms.Select(
            attrs={
                "class": "c-select",
                "x-model": "language",
            }
        ),
    )

    def clean_language(self):
        language = self.cleaned_data.get("language", "")
        if language:
            return Language[language]
        return None
