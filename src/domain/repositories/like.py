from abc import abstractmethod
from src.domain.repositories.base import CRUDRepository
from src.domain.entities import Like
from typing import Optional, List, Dict


class LikeRepository(CRUDRepository):
    @abstractmethod
    def like(self, like: Like): ...

    @abstractmethod
    def unlike(self, like: Like): ...

    @abstractmethod
    def get_like_if_exists(self, user_id: int, snippet_id: int) -> Optional[Like]: ...

    @abstractmethod
    def get_like_counts_for_snippets(
        self, snippet_ids: List[int]
    ) -> Dict[int, int]: ...

    @abstractmethod
    def get_like_status_for_snippets(
        self, user_id: int, snippet_ids: List[int]
    ) -> Dict[int, bool]: ...
