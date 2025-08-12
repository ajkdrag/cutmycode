from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from src.application.usecases.get_author_details import (
    GetAuthorDetailsRequest,
    GetAuthorDetailsResponse,
)
from src.application.usecases.get_author_snippet_previews import (
    GetAuthorSnippetsRequest,
    GetAuthorSnippetsResponse,
)
from src.interfaces.container import (
    get_author_details_uc,
    get_author_snippets_uc,
    get_principal,
)


from src.interfaces.web.forms.users import (
    UserCreationForm,
    UserEditForm,
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


def handle_author_detail(request, author_id):
    principal = get_principal(request)
    req = GetAuthorDetailsRequest(
        principal=principal,
        author_id=author_id,
    )
    author_resp: GetAuthorDetailsResponse = get_author_details_uc.execute(req)

    req = GetAuthorSnippetsRequest(
        principal=principal,
        author_id=author_id,
        limit=10,
        offset=0,
    )
    snippets_resp: GetAuthorSnippetsResponse = get_author_snippets_uc.execute(req)

    context = {
        "author": author_resp.author,
        "snippets": snippets_resp.snippets,
    }
    return render(request, "users/detail.html", context)
