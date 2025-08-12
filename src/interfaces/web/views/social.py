from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from src.application.usecases.create_share_link import (
    CreateShareLinkRequest,
    CreateShareLinkResponse,
)
from src.application.usecases.toggle_like import (
    ToggleLikeRequest,
)
from src.application.usecases.view_shared_snippet import (
    ViewSharedSnippetRequest,
)
from src.interfaces.container import (
    create_share_link_uc,
    get_principal,
    toggle_like_uc,
    view_shared_snippet_uc,
)


@login_required(login_url="login")
def handle_like_snippet(request, snippet_id):
    principal = get_principal(request)
    next_url = request.GET.get("next", f"/snippets/{snippet_id}/")

    if request.method == "POST":
        req = ToggleLikeRequest(
            principal=principal,
            snippet_id=snippet_id,
        )
        _ = toggle_like_uc.execute(req)
    return redirect(next_url)


@login_required(login_url="login")
def handle_share_snippet(request, snippet_id):
    principal = get_principal(request)

    if request.method != "POST":
        return redirect("snippet_detail", snippet_id=snippet_id)

    req = CreateShareLinkRequest(
        principal=principal,
        snippet_id=snippet_id,
        expires_in_hours=24,  # sane default (1 day)
    )

    try:
        resp: CreateShareLinkResponse = create_share_link_uc.execute(req)
        token = resp.share_link.token

        return redirect("share_link_created", token=token)
    except Exception as e:
        return render(request, "snippets/shared_error.html", {"error": str(e)})


@login_required(login_url="login")
def handle_share_link_created(request, token):
    share_url = request.build_absolute_uri(f"/share/{token}/")
    return render(request, "snippets/share.html", {"share_url": share_url})


def handle_view_shared_snippet(request, token):
    principal = get_principal(request)

    req = ViewSharedSnippetRequest(
        principal=principal,
        token=token,
    )

    try:
        resp = view_shared_snippet_uc.execute(req)
        context = {
            "snippet": resp.snippet,
            "share_link": resp.share_link,
            "is_shared_view": True,
        }
        return render(request, "snippets/shared.html", context)
    except Exception as e:
        print(e)
        return render(request, "snippets/shared_error.html", {"error": str(e)})
