from dataclasses import dataclass
from typing import List
from src.domain.types import SnippetId
from src.domain.entities import Comment
from src.domain.dtos import SnippetWithMetadata
from src.domain.ports.repositories import CommentRepository
from src.domain.ports.queries import SnippetsReadModel
from src.application.security import Principal
from src.domain.policies import SnippetPolicy


@dataclass(frozen=True)
class GetSnippetDetailsRequest:
    principal: Principal
    snippet_id: int


@dataclass(frozen=True)
class GetSnippetDetailsResponse:
    snippet: SnippetWithMetadata
    comments: List[Comment]


class GetSnippetDetails:
    def __init__(
        self,
        read_model: SnippetsReadModel,
        comment_repo: CommentRepository,
        snippet_policy: SnippetPolicy,
    ):
        self.read_model = read_model
        self.comment_repo = comment_repo
        self.snippet_policy = snippet_policy

    def execute(
        self,
        request: GetSnippetDetailsRequest,
    ) -> GetSnippetDetailsResponse:
        principal = request.principal
        user = principal.user
        snippet_id = SnippetId(request.snippet_id)

        user_id = None
        if principal.is_authenticated:
            user_id = user.id
            
        snippet_w_meta = self.read_model.get_with_meta(snippet_id, user_id)
        if not self.snippet_policy.can_view(user, snippet_w_meta):
            raise Exception("User is not allowed to view this snippet")

        comments = self.comment_repo.list_for_snippet(snippet_id)

        return GetSnippetDetailsResponse(
            snippet=snippet_w_meta,
            comments=comments,
        )
