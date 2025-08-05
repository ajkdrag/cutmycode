from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from src.application.security import Principal
from src.application.usecases.social import SocialUseCase
from src.data.orm.repositories.comment import DjangoCommentRepository
from src.data.orm.repositories.like import DjangolikeRepository
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.domain.policies import CommentPolicy, LikePolicy

comment_repo = DjangoCommentRepository()
like_repo = DjangolikeRepository()
snippet_repo = DjangoSnippetRepository()
user_repo = DjangoUserRepository()
like_policy = LikePolicy()
comment_policy = CommentPolicy()

social_uc = SocialUseCase(
    comment_repo=comment_repo,
    like_repo=like_repo,
    snippet_repo=snippet_repo,
    comment_policy=CommentPolicy(),
    like_policy=LikePolicy(),
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
