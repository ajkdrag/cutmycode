from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from src.application.security import Principal
from src.application.usecases.social import SocialUseCase
from src.data.orm.repositories.share import DjangoSharedSnippetRepository
from src.data.orm.repositories.comment import DjangoCommentRepository
from src.data.orm.repositories.like import DjangolikeRepository
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.domain.policies import CommentPolicy, LikePolicy, SharePolicy

shared_snippet_repo = DjangoSharedSnippetRepository()
comment_repo = DjangoCommentRepository()
like_repo = DjangolikeRepository()
snippet_repo = DjangoSnippetRepository()
user_repo = DjangoUserRepository()

like_policy = LikePolicy()
comment_policy = CommentPolicy()
share_policy = SharePolicy()

social_uc = SocialUseCase(
    comment_repo=comment_repo,
    like_repo=like_repo,
    snippet_repo=snippet_repo,
    shared_snippet_repo=shared_snippet_repo,
    comment_policy=CommentPolicy(),
    like_policy=LikePolicy(),
    share_policy=SharePolicy(),
)


@login_required(login_url="login")
def handle_like_snippet(request, snippet_id):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    next_url = request.GET.get("next")
    if request.method == "POST":
        social_uc.like_or_unlike_snippet(
            principal=principal,
            snippet_id=snippet_id,
        )
    return redirect(next_url)


@login_required(login_url="login")
def handle_share_snippet(request, snippet_id):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    next_url = request.GET.get("next")
    if request.method == "POST":
        token = social_uc.share_snippet(
            principal=principal,
            snippet_id=snippet_id,
        )
        share_url = request.build_absolute_uri(f"/share/{token}")
        return redirect(share_url)
    return redirect(next_url)


def handle_view_shared_snippet(request, token):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    shared_snippet = social_uc.get_shared_snippet(
        principal=principal,
        token=token,
    )
    context = {
        "snippet": shared_snippet.snippet,
    }
    return render(request, "snippets/share.html", context)
