from typing import Dict, List, Optional

from django.db.models import Count

from src.data.orm.models import Like as LikeModel
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.domain.entities import Like
from src.domain.repositories.like import LikeRepository


class DjangolikeRepository(LikeRepository):
    @staticmethod
    def _from_orm(like_model: LikeModel) -> Like:
        user_model = like_model.user
        snippet_model = like_model.snippet

        user = DjangoUserRepository._from_orm(user_model)
        snippet = DjangoSnippetRepository._from_orm(snippet_model)

        return Like(
            id=like_model.id,
            user=user,
            snippet=snippet,
            created_at=like_model.created_at,
            updated_at=like_model.updated_at,
        )

    def get(self, id: int) -> Like:
        like_model = LikeModel.objects.select_related(
            "user",
            "snippet__author",
        ).get(id=id)
        return self._from_orm(like_model)

    def create(self, like: Like):
        like_model = LikeModel(
            user_id=like.user.id,
            snippet_id=like.snippet.id,
        )
        like_model.full_clean()
        like_model.save()

    def update(self, like: Like):
        like_model = LikeModel.objects.get(id=like.id)
        like_model.full_clean()
        like_model.save()

    def delete(self, id: int) -> bool:
        try:
            like_model = LikeModel.objects.get(id=id)
            like_model.delete()
            return True
        except LikeModel.DoesNotExist:
            return False

    def get_like_counts_for_snippet(self, snippet_id: int) -> int:
        return LikeModel.objects.filter(snippet_id=snippet_id).count()

    def like(self, like: Like):
        self.create(like)

    def unlike(self, like: Like):
        self.delete(like.id)

    def get_like_if_exists(
        self,
        user_id: int,
        snippet_id: int,
    ) -> Optional[Like]:
        try:
            like_model = LikeModel.objects.get(
                user_id=user_id,
                snippet_id=snippet_id,
            )
            return self._from_orm(like_model)
        except LikeModel.DoesNotExist:
            return None

    def get_like_counts_for_snippets(self, snippet_ids: List[int]) -> Dict[int, int]:
        like_counts = (
            LikeModel.objects.filter(
                snippet_id__in=snippet_ids,
            )
            .values("snippet_id")
            .annotate(count=Count("id"))
            .values_list("snippet_id", "count")
        )
        return dict(like_counts)

    def get_like_status_for_snippets(
        self, user_id: int, snippet_ids: List[int]
    ) -> Dict[int, bool]:
        liked_snippet_ids = LikeModel.objects.filter(
            user_id=user_id,
            snippet_id__in=snippet_ids,
        ).values_list("snippet_id", flat=True)

        def liked(snippet_id: int) -> bool:
            return snippet_id in liked_snippet_ids

        return {snippet_id: liked(snippet_id) for snippet_id in snippet_ids}
