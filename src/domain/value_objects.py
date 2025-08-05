from dataclasses import dataclass
from typing import List, Optional

from src.domain.constants import Language
from src.domain.entities import Snippet


@dataclass(kw_only=True)
class SnippetStats:
    like_count: int
    comment_count: int


@dataclass(kw_only=True)
class UserSnippetInteractions:
    liked: bool
    commented: bool


@dataclass(kw_only=True)
class SnippetMetadata:
    stats: SnippetStats
    interactions: Optional[UserSnippetInteractions] = None


@dataclass(kw_only=True)
class SnippetWithMetadata(Snippet):
    metadata: SnippetMetadata


@dataclass(kw_only=True)
class SearchQuery:
    query: str
    language: Optional[Language] = None

    def is_empty(self) -> bool:
        return not (self.query or self.language)


@dataclass(kw_only=True)
class SearchResult:
    snippets: List[Snippet]
