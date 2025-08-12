from dataclasses import dataclass
from typing import List

from src.domain.dtos import SnippetWithMetadata
from src.domain.entities import User
from src.domain.ports.queries import SnippetsReadModel
from src.domain.value_objects import SearchQuery
from src.application.security import Principal


@dataclass(frozen=True)
class GetSearchResultsRequest:
    principal: Principal
    query: SearchQuery
    limit: int
    offset: int


@dataclass(frozen=True)
class GetSearchResultsResponse:
    snippets: List[SnippetWithMetadata]
    users: List[User]


class GetSearchResults:
    def __init__(
        self,
        read_model: SnippetsReadModel,
    ):
        self.read_model = read_model

    def execute(
        self,
        request: GetSearchResultsRequest,
    ) -> GetSearchResultsResponse:
        user_id = None
        if request.principal.is_authenticated:
            user_id = request.principal.user.id

        found_snippets = self.read_model.search_snippets(
            search_text=request.query.text,
            language=request.query.language,
            user_id=user_id,
            limit=request.limit,
            offset=request.offset,
        )

        return GetSearchResultsResponse(
            snippets=found_snippets,
            users=[],
        )
