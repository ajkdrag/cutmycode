from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from src.application.security import Principal
from src.domain.entities import Snippet, SnippetShareLink, SnippetShareLinkDraft
from src.domain.policies import SharePolicy, SnippetPolicy
from src.domain.ports.repositories import SnippetRepository, SnippetShareLinkRepository
from src.domain.types import SnippetId


@dataclass(frozen=True)
class CreateShareLinkRequest:
    principal: Principal
    snippet_id: int
    expires_in_hours: int = 24  # Default 24 hours


@dataclass(frozen=True)
class CreateShareLinkResponse:
    share_link: SnippetShareLink
    snippet: Snippet


class CreateShareLink:
    def __init__(
        self,
        snippet_repo: SnippetRepository,
        share_link_repo: SnippetShareLinkRepository,
        snippet_policy: SnippetPolicy,
        share_policy: SharePolicy,
    ):
        self.snippet_repo = snippet_repo
        self.share_link_repo = share_link_repo
        self.snippet_policy = snippet_policy
        self.share_policy = share_policy

    def execute(
        self,
        request: CreateShareLinkRequest,
    ) -> CreateShareLinkResponse:
        principal = request.principal
        user = principal.user
        snippet_id = SnippetId(request.snippet_id)

        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        snippet = self.snippet_repo.get(snippet_id)
        if not snippet:
            raise Exception("Snippet not found")

        if not self.share_policy.can_share(user, snippet):
            raise Exception("User is not allowed to share this snippet")

        expires_at = datetime.now(tz=timezone.utc) + timedelta(
            hours=request.expires_in_hours
        )

        draft = SnippetShareLinkDraft(
            snippet_id=snippet_id,
            shared_by_id=user.id,
            expires_at=expires_at,
        )
        share_link = self.share_link_repo.add(draft)
        return CreateShareLinkResponse(share_link=share_link, snippet=snippet)

