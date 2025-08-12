from dataclasses import dataclass
from src.domain.entities import Snippet, SnippetShareLink
from src.domain.ports.repositories import (
    SnippetRepository,
    SnippetShareLinkRepository,
)
from src.application.security import Principal


@dataclass(frozen=True)
class ViewSharedSnippetRequest:
    principal: Principal
    token: str


@dataclass(frozen=True)
class ViewSharedSnippetResponse:
    snippet: Snippet
    share_link: SnippetShareLink


class ViewSharedSnippet:
    def __init__(
        self,
        snippet_repo: SnippetRepository,
        share_link_repo: SnippetShareLinkRepository,
    ):
        self.snippet_repo = snippet_repo
        self.share_link_repo = share_link_repo

    def execute(
        self,
        request: ViewSharedSnippetRequest,
    ) -> ViewSharedSnippetResponse:
        # Clean up expired links first (can be moved to a background task)
        self.share_link_repo.deactivate_expired()

        share_link = self.share_link_repo.get_by_token(request.token)
        if not share_link:
            raise Exception("Share link not found")

        if not share_link.is_valid:
            raise Exception("Share link has expired or is no longer active")

        snippet = self.snippet_repo.get(share_link.snippet_id)
        if not snippet:
            raise Exception("Snippet not found")

        return ViewSharedSnippetResponse(
            snippet=snippet,
            share_link=share_link,
        )

