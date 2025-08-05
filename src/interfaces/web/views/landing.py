from django.shortcuts import render
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.data.orm.repositories.like import DjangolikeRepository
from src.data.orm.repositories.comment import DjangoCommentRepository
from src.domain.policies import SnippetPolicy
from src.application.usecases.snippets import SnippetsUseCase
from src.application.security import Principal
from src.application.dtos import SearchResultsDTO, ListSnippetsDTO
from src.interfaces.web.forms.search import SearchForm


snippet_repo = DjangoSnippetRepository()
user_repo = DjangoUserRepository()
comment_repo = DjangoCommentRepository()
like_repo = DjangolikeRepository()
snippet_policy = SnippetPolicy()

snippets_uc = SnippetsUseCase(
    snippet_repo=snippet_repo,
    like_repo=like_repo,
    comment_repo=comment_repo,
    snippet_policy=SnippetPolicy(),
)


def handle_landing(request):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    search_form = SearchForm(request.GET or None)
    search_query = None
    search_performed = False

    if search_form.is_valid():
        search_query = search_form.get_search_query()
        search_performed = not search_query.is_empty()

    if search_performed:
        search_resp: SearchResultsDTO = snippets_uc.search_snippets(
            principal=principal,
            search_query=search_query,
            with_meta=True,
        )

        context = {
            "snippets": search_resp.snippets,
            "search_form": search_form,
            "query": search_query.query,
            "search_performed": search_performed,
        }
    else:
        resp: ListSnippetsDTO = snippets_uc.get_visible_snippets(
            principal=principal,
            with_meta=True,
        )
        context = {
            "snippets": resp.snippets,
            "search_form": search_form,
            "search_performed": search_performed,
        }

    return render(request, "public/landing.html", context)
