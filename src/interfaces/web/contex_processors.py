from src.interfaces.web.forms.search import SearchForm


def search_form(request):
    return {
        "search_form": SearchForm(),
    }
