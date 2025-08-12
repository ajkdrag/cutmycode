from dataclasses import dataclass
from src.domain.types import SnippetId
from src.domain.ports.repositories import LikeRepository, SnippetRepository
from src.application.security import Principal
from src.domain.policies import LikePolicy


@dataclass(frozen=True)
class ToggleLikeRequest:
    principal: Principal
    snippet_id: int


@dataclass(frozen=True)
class ToggleLikeResponse:
    liked: bool  # True if now liked, False if now unliked


class ToggleLike:
    def __init__(
        self,
        like_repo: LikeRepository,
        snippet_repo: SnippetRepository,
        like_policy: LikePolicy,
    ):
        self.like_repo = like_repo
        self.snippet_repo = snippet_repo
        self.like_policy = like_policy

    def execute(
        self,
        request: ToggleLikeRequest,
    ) -> ToggleLikeResponse:
        principal = request.principal
        user = principal.user
        snippet_id = SnippetId(request.snippet_id)

        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        snippet = self.snippet_repo.get(snippet_id)
        if not snippet:
            raise Exception("Snippet not found")

        if not self.like_policy.can_like_or_unlike(user, snippet):
            raise Exception("User is not allowed to like snippets")

        is_currently_liked = self.like_repo.is_liked(user.id, snippet_id)

        if is_currently_liked:
            self.like_repo.delete(user.id, snippet_id)
            return ToggleLikeResponse(liked=False)
        else:
            self.like_repo.add(user.id, snippet_id)
            return ToggleLikeResponse(liked=True)

