from dataclasses import dataclass
from src.domain.constants import Language
from datetime import datetime, timezone
from typing import Optional


@dataclass(kw_only=True)
class Entity:
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass(kw_only=True)
class User(Entity):
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    about: Optional[str] = None
    is_active: bool = True


@dataclass(kw_only=True)
class AnonymousUser(User):
    username: str = ""
    email: str = ""
    is_active: bool = False


@dataclass(kw_only=True)
class Snippet(Entity):
    title: str
    code: str
    description: Optional[str] = None
    language: Language
    is_public: bool
    author: User


@dataclass(kw_only=True)
class SharedSnippet(Entity):
    snippet: Snippet
    token: str
    expires_at: datetime
    is_active: bool = True
    created_by: User

    @property
    def has_expired(self) -> bool:
        now = datetime.now(tz=timezone.utc)
        return now > self.expires_at

    @property
    def is_valid(self) -> bool:
        return self.is_active and not self.has_expired


@dataclass(kw_only=True)
class Comment(Entity):
    body: str
    author: User
    snippet: Snippet
    is_deleted: bool = False


@dataclass(kw_only=True)
class Like(Entity):
    user: User
    snippet: Snippet
