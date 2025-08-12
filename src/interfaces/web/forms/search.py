from django import forms
from src.domain.constants import Language
from src.domain.value_objects import SearchQuery


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search snippets...",
                "class": "c-input",
            }
        ),
        label="",
    )

    language = forms.ChoiceField(
        choices=[("", "All Languages")] + Language.choices(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "c-select",
            }
        ),
        label="",
    )

    def clean_query(self):
        query = self.cleaned_data.get("query", "").strip()
        return query

    def clean_language(self):
        language = self.cleaned_data.get("language", "")
        if language:
            return Language[language]
        return None

    def get_search_query(self) -> SearchQuery:
        self.full_clean()
        return SearchQuery(
            text=self.cleaned_data.get("query", ""),
            language=self.cleaned_data.get("language", ""),
        )
