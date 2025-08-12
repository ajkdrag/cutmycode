from django.shortcuts import render, redirect

from src.application.usecases.get_search_results import (
    GetSearchResultsRequest,
    GetSearchResultsResponse,
)
from src.domain.value_objects import SearchQuery
from src.interfaces.web.forms.search import SearchForm
from src.interfaces.container import get_principal, get_search_results_uc


def handle_search(request):
    principal = get_principal(request)
    form = SearchForm(request.GET)
    search_query: SearchQuery = form.get_search_query()

    if not form.is_valid() or search_query.is_empty():
        return redirect(request.META.get("HTTP_REFERER", "/"))

    req = GetSearchResultsRequest(
        principal=principal,
        query=search_query,
        limit=10,
        offset=0,
    )

    resp: GetSearchResultsResponse = get_search_results_uc.execute(req)
    context = {
        "snippets": resp.snippets,
        "results_count": len(resp.snippets),
        "search_form": form,
    }

    return render(request, "search/results.html", context)

