from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from src.application.usecases.get_snippet_details import (
    GetSnippetDetailsRequest,
    GetSnippetDetailsResponse,
)
from src.application.usecases.create_snippet import (
    CreateSnippetRequest,
)
from src.application.usecases.update_snippet import (
    UpdateSnippetRequest,
)
from src.application.usecases.get_user_snippet_previews import (
    GetUserSnippetsRequest,
    GetUserSnippetsResponse,
)
from src.application.usecases.create_comment import (
    CreateCommentRequest,
    CreateCommentResponse,
)
from src.interfaces.container import (
    get_snippet_details_uc,
    create_snippet_uc,
    update_snippet_uc,
    get_user_snippets_uc,
    create_comment_uc,
    get_principal,
    snippet_policy,
)
from src.interfaces.web.forms.snippets import SnippetCreationForm
from src.interfaces.web.forms.social import CommentForm


def handle_snippet_detail(request, snippet_id):
    principal = get_principal(request)
    req = GetSnippetDetailsRequest(
        principal=principal,
        snippet_id=snippet_id,
    )
    resp: GetSnippetDetailsResponse = get_snippet_details_uc.execute(req)
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
            req = CreateCommentRequest(
                principal=principal,
                snippet_id=snippet_id,
                body=comment_form.cleaned_data["body"],
            )
            try:
                resp: CreateCommentResponse = create_comment_uc.execute(req)
                return redirect("snippet_detail", snippet_id=snippet_id)
            except Exception as e:
                comment_form.add_error("body", str(e))

    context = {
        "snippet": resp.snippet,
        "comments": resp.comments,
        "can_edit": can_edit,
        "comment_form": comment_form,
    }
    return render(request, "snippets/detail.html", context)


@login_required(login_url="login")
def handle_create_snippet(request):
    principal = get_principal(request)

    form = SnippetCreationForm(request.POST or None)
    if form.is_valid():
        req = CreateSnippetRequest(
            principal=principal,
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            code=form.cleaned_data["code"],
            language=form.cleaned_data["language"],
            is_public=True,
        )
        _ = create_snippet_uc.execute(req)
        return redirect("landing_page")
    return render(request, "snippets/create.html", {"form": form})


@login_required(login_url="login")
def handle_edit_snippet(request, snippet_id):
    principal = get_principal(request)

    # Get snippet details to check permissions and populate form
    req = GetSnippetDetailsRequest(
        principal=principal,
        snippet_id=snippet_id,
    )
    resp: GetSnippetDetailsResponse = get_snippet_details_uc.execute(req)

    if not snippet_policy.can_edit(principal.user, resp.snippet):
        return HttpResponseForbidden("Not allowed to edit this snippet")

    form = SnippetCreationForm(
        request.POST or None,
        initial={
            "title": resp.snippet.title,
            "description": resp.snippet.description,
            "code": resp.snippet.code,
            "language": resp.snippet.language.name,
        },
    )

    if request.method == "POST" and form.is_valid():
        update_req = UpdateSnippetRequest(
            principal=principal,
            snippet_id=snippet_id,
            title=form.cleaned_data["title"],
            description=form.cleaned_data["description"],
            code=form.cleaned_data["code"],
            language=form.cleaned_data["language"],
            is_public=True,
        )
        _ = update_snippet_uc.execute(update_req)
        return redirect("snippet_detail", snippet_id=snippet_id)
    return render(request, "snippets/edit.html", {"form": form})


@login_required(login_url="login")
def handle_my_snippets(request):
    principal = get_principal(request)
    req = GetUserSnippetsRequest(
        principal=principal,
        limit=20,
        offset=0,
    )
    resp: GetUserSnippetsResponse = get_user_snippets_uc.execute(req)
    context = {
        "snippets": resp.snippets,
    }
    return render(request, "snippets/my_snippets.html", context)
