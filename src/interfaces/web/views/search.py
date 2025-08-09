from django.shortcuts import render, redirect

from src.application.dtos import SearchResultsDTO
from src.application.security import Principal
from src.application.usecases.snippets import SnippetsUseCase
from src.data.orm.repositories.comment import DjangoCommentRepository
from src.data.orm.repositories.like import DjangolikeRepository
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.domain.policies import SnippetPolicy
from src.domain.value_objects import SearchQuery
from src.interfaces.web.forms.search import SearchForm


snippet_repo = DjangoSnippetRepository()
user_repo = DjangoUserRepository()
comment_repo = DjangoCommentRepository()
like_repo = DjangolikeRepository()

snippets_uc = SnippetsUseCase(
    snippet_repo=snippet_repo,
    like_repo=like_repo,
    comment_repo=comment_repo,
    snippet_policy=SnippetPolicy(),
)


def handle_search(request):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    form = SearchForm(request.GET)
    search_query: SearchQuery = form.get_search_query()

    if not form.is_valid() or search_query.is_empty():
        return redirect(request.META.get("HTTP_REFERER", "/"))

    search_resp: SearchResultsDTO = snippets_uc.search_snippets(
        principal=principal,
        search_query=search_query,
        with_meta=True,
    )
    snippets = search_resp.snippets

    context = {
        "snippets": snippets,
        "results_count": len(snippets),
        "search_form": form,
    }

    return render(request, "search/results.html", context)

