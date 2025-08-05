from django import forms
from src.domain.constants import Language
from src.domain.value_objects import SearchQuery


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search snippets...",
                "class": "search-input",
            }
        ),
    )

    language = forms.ChoiceField(
        choices=[("", "All Languages")] + Language.choices(),
        required=False,
        widget=forms.Select(
            attrs={
                "class": "language-filter",
            }
        ),
    )

    def clean_query(self):
        query = self.cleaned_data.get("query", "").strip()
        return query

    def get_search_query(self) -> SearchQuery:
        return SearchQuery(
            query=self.cleaned_data.get("query", "").strip(),
            language=self.cleaned_data.get("language", ""),
        )

