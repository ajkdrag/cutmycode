from abc import abstractmethod
from typing import Optional

from src.domain.entities import SharedSnippet
from src.domain.repositories.base import CRUDRepository


class SharedSnippetRepository(CRUDRepository):
    @abstractmethod
    def get_by_token(self, token: str) -> Optional[SharedSnippet]: ...

    @abstractmethod
    def deactivate_expired_shares(self) -> None: ...
