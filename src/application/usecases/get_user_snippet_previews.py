from dataclasses import dataclass
from typing import List
from src.domain.dtos import SnippetWithMetadata
from src.domain.ports.queries import SnippetsReadModel
from src.application.security import Principal


@dataclass(frozen=True)
class GetUserSnippetsRequest:
    principal: Principal
    limit: int
    offset: int


@dataclass(frozen=True)
class GetUserSnippetsResponse:
    snippets: List[SnippetWithMetadata]


class GetUserSnippets:
    def __init__(self, read_model: SnippetsReadModel):
        self.read_model = read_model

    def execute(
        self,
        request: GetUserSnippetsRequest,
    ) -> GetUserSnippetsResponse:
        principal = request.principal
        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        return GetUserSnippetsResponse(
            snippets=self.read_model.list_from_user_with_meta(
                user_id=principal.user.id,
                limit=request.limit,
                offset=request.offset,
            )
        )
