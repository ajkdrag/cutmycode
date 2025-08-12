from typing import List, Protocol
from src.domain.types import UserId, SnippetId
from src.domain.dtos import SnippetWithMetadata


class SnippetsReadModel(Protocol):
    def get_with_meta(
        self, snippet_id: SnippetId, user_id: UserId | None = None
    ) -> SnippetWithMetadata: ...

    def list_public_with_meta(
        self, user_id: UserId | None = None, limit: int = 10, offset: int = 0
    ) -> List[SnippetWithMetadata]: ...

    def list_from_author_with_meta(
        self,
        author_id: UserId,
        user_id: UserId | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[SnippetWithMetadata]:
        """Public snippets from author"""

    def list_from_user_with_meta(
        self,
        user_id: UserId,
        limit: int = 10,
        offset: int = 0,
    ) -> List[SnippetWithMetadata]:
        """Snippets from user (public + private)"""

    def search_snippets(
        self,
        search_text: str,
        language: str | None = None,
        user_id: UserId | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[SnippetWithMetadata]:
        """Search across public snippets"""
