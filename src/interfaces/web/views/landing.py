from django.shortcuts import render
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.data.orm.repositories.like import DjangolikeRepository
from src.data.orm.repositories.comment import DjangoCommentRepository
from src.domain.policies import SnippetPolicy
from src.application.usecases.snippets import SnippetsUseCase
from src.application.security import Principal
from src.application.dtos import ListSnippetsDTO


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

    resp: ListSnippetsDTO = snippets_uc.get_visible_snippets(
        principal=principal,
        with_meta=True,
    )

    context = {
        "snippets": resp.snippets,
    }

    return render(request, "public/landing.html", context)
