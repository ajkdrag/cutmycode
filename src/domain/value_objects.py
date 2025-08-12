from dataclasses import dataclass

from src.domain.constants import Language
from src.domain.types import UserId


@dataclass(frozen=True)
class AuthorRef:
    id: UserId
    username: str | None = None


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
    interactions: UserSnippetInteractions | None = None


@dataclass(kw_only=True)
class SearchQuery:
    text: str
    language: Language | None = None

    def is_empty(self) -> bool:
        return not (self.text or self.language)
