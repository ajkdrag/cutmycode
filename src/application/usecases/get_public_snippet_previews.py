from dataclasses import dataclass
from typing import List
from src.domain.dtos import SnippetWithMetadata
from src.domain.ports.queries import SnippetsReadModel
from src.application.security import Principal


@dataclass(frozen=True)
class GetPublicSnippetsRequest:
    principal: Principal
    limit: int
    offset: int


@dataclass(frozen=True)
class GetPublicSnippetsResponse:
    snippets: List[SnippetWithMetadata]


class GetPublicSnippets:
    def __init__(self, read_model: SnippetsReadModel):
        self.read_model = read_model

    def execute(
        self,
        request: GetPublicSnippetsRequest,
    ) -> GetPublicSnippetsResponse:
        user_id = None
        if request.principal.is_authenticated:
            user_id = request.principal.user.id
            
        return GetPublicSnippetsResponse(
            snippets=self.read_model.list_public_with_meta(
                user_id=user_id,
                limit=request.limit,
                offset=request.offset,
            )
        )
