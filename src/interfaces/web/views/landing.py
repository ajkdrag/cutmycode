from django.shortcuts import render
from src.application.usecases.get_public_snippet_previews import (
    GetPublicSnippetsRequest,
    GetPublicSnippetsResponse,
)
from src.interfaces.container import get_public_snippets_uc, get_principal


def handle_landing(request):
    principal = get_principal(request)
    req = GetPublicSnippetsRequest(
        principal=principal,
        limit=10,
        offset=0,
    )

    resp: GetPublicSnippetsResponse = get_public_snippets_uc.execute(req)
    context = {
        "snippets": resp.snippets,
    }

    return render(request, "public/landing.html", context)
