from abc import abstractmethod
from typing import List

from src.domain.value_objects import (
    SearchQuery,
    SearchResult,
)
from src.domain.entities import Snippet
from src.domain.repositories.base import CRUDRepository


class SnippetRepository(CRUDRepository):
    @abstractmethod
    def get_public_snippets(self) -> List[Snippet]: ...

    @abstractmethod
    def get_user_private_snippets(self, user_id: int) -> List[Snippet]: ...

    @abstractmethod
    def get_user_snippets(
        self,
        user_id: int,
        only_public: bool = False,
    ) -> List[Snippet]: ...

    @abstractmethod
    def get_snippet_by_id(self, snippet_id: int) -> Snippet: ...

    @abstractmethod
    def get_visible_snippets(self, user_id: int) -> List[Snippet]: ...

    @abstractmethod
    def search_across_public_snippets(
        self, search_query: SearchQuery
    ) -> SearchResult: ...

    @abstractmethod
    def search_across_visible_snippets(
        self, search_query: SearchQuery, user_id: int
    ) -> SearchResult:
        """Search all snippets accessible to user (public + own private)"""
        ...
