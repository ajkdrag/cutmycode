from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from src.application.dtos import ListSnippetsDTO, SnippetDetailDTO
from src.application.security import Principal
from src.application.usecases.snippets import SnippetsUseCase
from src.application.usecases.social import SocialUseCase
from src.data.orm.repositories.comment import DjangoCommentRepository
from src.data.orm.repositories.like import DjangolikeRepository
from src.data.orm.repositories.share import DjangoSharedSnippetRepository
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.domain.policies import (
    CommentPolicy,
    LikePolicy,
    SharePolicy,
    SnippetPolicy,
)
from src.interfaces.web.forms.snippets import SnippetCreationForm
from src.interfaces.web.forms.social import CommentForm

snippet_repo = DjangoSnippetRepository()
user_repo = DjangoUserRepository()
comment_repo = DjangoCommentRepository()
shared_snippet_repo = DjangoSharedSnippetRepository()
like_repo = DjangolikeRepository()
snippet_policy = SnippetPolicy()
share_policy = SharePolicy()

snippets_uc = SnippetsUseCase(
    snippet_repo=snippet_repo,
    like_repo=like_repo,
    comment_repo=comment_repo,
    snippet_policy=SnippetPolicy(),
)

social_uc = SocialUseCase(
    comment_repo=comment_repo,
    like_repo=like_repo,
    snippet_repo=snippet_repo,
    shared_snippet_repo=shared_snippet_repo,
    comment_policy=CommentPolicy(),
    share_policy=SharePolicy(),
    like_policy=LikePolicy(),
)


def handle_snippet_detail(request, snippet_id):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    resp: SnippetDetailDTO = snippets_uc.get_snippet_detail(
        principal=principal,
        snippet_id=snippet_id,
        with_meta=True,
    )
    can_edit = snippet_policy.can_edit(principal.user, resp.snippet)

    comment_form = CommentForm(
        request.session.pop("saved_comment_data", None),
    )

    if request.method == "POST":
        if not principal.is_authenticated:
            request.session["saved_comment_data"] = request.POST
            return redirect_to_login(
                next=request.get_full_path(),
                login_url="login",
            )
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            social_uc.create_comment(
                principal=principal,
                body=comment_form.cleaned_data["body"],
                snippet_id=snippet_id,
            )
            return redirect("snippet_detail", snippet_id=snippet_id)

    context = {
        "snippet": resp.snippet,
        "comments": resp.comments,
        "can_edit": can_edit,
        "comment_form": comment_form,
    }
    return render(request, "snippets/detail.html", context)


@login_required(login_url="login")
def handle_create_snippet(request):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    form = SnippetCreationForm(request.POST or None)
    if form.is_valid():
        snippets_uc.create_snippet(
            principal=principal,
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            code=form.cleaned_data["code"],
            language=form.cleaned_data["language"],
            is_public=True,
        )
        return redirect("landing_page")
    return render(request, "snippets/create.html", {"form": form})


@login_required(login_url="login")
def handle_edit_snippet(request, snippet_id):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    resp: SnippetDetailDTO = snippets_uc.get_snippet_detail(
        principal=principal,
        snippet_id=snippet_id,
        with_meta=False,
    )

    if not snippet_policy.can_edit(user, resp.snippet):
        return HttpResponseForbidden("Not allowed to edit this snippet")

    form = SnippetCreationForm(
        request.POST or None,
        initial={
            "title": resp.snippet.title,
            "description": resp.snippet.description,
            "code": resp.snippet.code,
            "language": resp.snippet.language,
        },
    )

    if request.method == "POST" and form.is_valid():
        snippets_uc.update_snippet(
            principal=principal,
            snippet_id=snippet_id,
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            code=form.cleaned_data["code"],
            language=form.cleaned_data["language"],
            is_public=True,
        )
        return redirect("snippet_detail", snippet_id=snippet_id)
    return render(request, "snippets/edit.html", {"form": form})


@login_required(login_url="login")
def handle_my_snippets(request):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    resp: ListSnippetsDTO = snippets_uc.get_user_snippets(
        principal=principal,
        with_meta=True,
    )
    context = {
        "snippets": resp.snippets,
    }
    return render(request, "snippets/my_snippets.html", context)
