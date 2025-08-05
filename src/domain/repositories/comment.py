from abc import abstractmethod
from typing import List, Dict
from src.domain.repositories.base import CRUDRepository
from src.domain.entities import Comment


class CommentRepository(CRUDRepository):
    @abstractmethod
    def get_comments_for_snippet(self, snippet_id: int) -> List[Comment]: ...

    @abstractmethod
    def get_comment_counts_for_snippets(
        self, snippet_ids: List[int]
    ) -> Dict[int, int]: ...
