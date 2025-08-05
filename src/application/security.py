from dataclasses import dataclass
from src.domain.entities import User, AnonymousUser


@dataclass(kw_only=True, frozen=True)
class Principal:
    user: User
    is_authenticated: bool

    @classmethod
    def anonymous(cls):
        return cls(user=AnonymousUser(), is_authenticated=False)

    @classmethod
    def authenticated(cls, user: User):
        return cls(user=user, is_authenticated=True)
