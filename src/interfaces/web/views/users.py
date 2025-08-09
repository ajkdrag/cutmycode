from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from src.application.usecases.users import UsersUseCase
from src.domain.policies import SnippetPolicy, UserInteractionPolicy
from src.data.orm.repositories.comment import DjangoCommentRepository
from src.data.orm.repositories.like import DjangolikeRepository
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.application.security import Principal
from src.application.dtos import UserDetailDTO


from src.interfaces.web.forms.users import (
    UserCreationForm,
    UserEditForm,
)


snippet_repo = DjangoSnippetRepository()
user_repo = DjangoUserRepository()
comment_repo = DjangoCommentRepository()
like_repo = DjangolikeRepository()

users_uc = UsersUseCase(
    user_repo=user_repo,
    snippet_repo=snippet_repo,
    like_repo=like_repo,
    comment_repo=comment_repo,
    snippet_policy=SnippetPolicy(),
    user_interaction_policy=UserInteractionPolicy(),
)


def handle_signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "registration/signup.html", {"form": form})


@login_required(login_url="login")
def handle_edit_profile(request):
    form = UserEditForm(
        request.POST or None,
        instance=request.user,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("my_snippets")
    return render(request, "users/edit_profile.html", {"form": form})


def handle_user_detail(request, user_id):
    principal = Principal.anonymous()
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        principal = Principal.authenticated(user)

    resp: UserDetailDTO = users_uc.get_user_detail(
        principal=principal,
        user_id=user_id,
        with_meta=True,
    )
    context = {
        "viewed_user": resp.user,
        "snippets": resp.snippets,
    }
    return render(request, "users/detail.html", context)
