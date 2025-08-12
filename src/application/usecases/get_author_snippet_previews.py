from dataclasses import dataclass
from typing import List
from src.domain.types import UserId
from src.domain.dtos import SnippetWithMetadata
from src.domain.ports.queries import SnippetsReadModel
from src.application.security import Principal


@dataclass(frozen=True)
class GetAuthorSnippetsRequest:
    principal: Principal
    author_id: int
    limit: int
    offset: int


@dataclass(frozen=True)
class GetAuthorSnippetsResponse:
    snippets: List[SnippetWithMetadata]


class GetAuthorSnippets:
    def __init__(self, read_model: SnippetsReadModel):
        self.read_model = read_model

    def execute(
        self,
        request: GetAuthorSnippetsRequest,
    ) -> GetAuthorSnippetsResponse:
        author_id = UserId(request.author_id)
        user_id = None
        if request.principal.is_authenticated:
            user_id = request.principal.user.id
            
        return GetAuthorSnippetsResponse(
            snippets=self.read_model.list_from_author_with_meta(
                author_id=author_id,
                user_id=user_id,
                limit=request.limit,
                offset=request.offset,
            )
        )
