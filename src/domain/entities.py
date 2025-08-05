from dataclasses import dataclass
from src.domain.constants import Language
from datetime import datetime
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
class Comment(Entity):
    body: str
    author: User
    snippet: Snippet
    is_deleted: bool = False


@dataclass(kw_only=True)
class Like(Entity):
    user: User
    snippet: Snippet
