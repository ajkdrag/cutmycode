from dataclasses import dataclass
from src.domain.constants import Language
from datetime import datetime, timezone
from src.domain.types import (
    UserId,
    SnippetId,
    CommentId,
    LikeId,
    SnippetShareLinkId,
)
from src.domain.value_objects import AuthorRef


@dataclass(kw_only=True)
class User:
    id: UserId
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    about: str | None = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime | None = None


@dataclass(kw_only=True)
class AnonymousUser: ...


@dataclass(kw_only=True)
class SnippetDraft:
    author_id: UserId
    title: str
    code: str
    description: str | None = None
    language: Language
    is_public: bool


@dataclass(kw_only=True)
class Snippet:
    id: SnippetId
    author: AuthorRef
    title: str
    code: str
    description: str | None = None
    language: Language
    is_public: bool
    created_at: datetime
    updated_at: datetime | None = None


@dataclass(kw_only=True)
class SnippetShareLinkDraft:
    snippet_id: SnippetId
    shared_by_id: UserId
    expires_at: datetime


@dataclass(kw_only=True)
class SnippetShareLink:
    id: SnippetShareLinkId
    snippet_id: SnippetId
    shared_by: AuthorRef
    token: str
    expires_at: datetime
    is_active: bool = True
    created_at: datetime
    updated_at: datetime | None = None

    @property
    def has_expired(self) -> bool:
        now = datetime.now(tz=timezone.utc)
        return now > self.expires_at

    @property
    def is_valid(self) -> bool:
        return self.is_active and not self.has_expired


@dataclass(kw_only=True)
class CommentDraft:
    author_id: UserId
    snippet_id: SnippetId
    body: str


@dataclass(kw_only=True)
class Comment:
    id: CommentId
    author: AuthorRef
    snippet_id: SnippetId
    body: str
    is_deleted: bool = False
    created_at: datetime
    updated_at: datetime | None = None


@dataclass(kw_only=True)
class LikeDraft:
    user_id: UserId
    snippet_id: SnippetId


@dataclass(kw_only=True)
class Like:
    id: LikeId
    user_id: UserId
    snippet_id: SnippetId
    created_at: datetime
    updated_at: datetime | None = None
