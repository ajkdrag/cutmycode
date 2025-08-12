from django.db import IntegrityError
from src.domain.types import UserId, SnippetId
from src.data.orm.models import Like as LikeM


class DjangoLikeRepository:
    def add(self, user_id: UserId, snippet_id: SnippetId) -> None:
        try:
            like_model = LikeM(
                user_id=user_id,
                snippet_id=snippet_id,
            )
            like_model.full_clean()
            like_model.save()
        except IntegrityError:
            # Like already exists, ignore
            pass

    def delete(self, user_id: UserId, snippet_id: SnippetId) -> None:
        LikeM.objects.filter(
            user_id=user_id,
            snippet_id=snippet_id,
        ).delete()

    def is_liked(self, user_id: UserId, snippet_id: SnippetId) -> bool:
        return LikeM.objects.filter(
            user_id=user_id,
            snippet_id=snippet_id,
        ).exists()

    def count_for_snippet(self, snippet_id: SnippetId) -> int:
        return LikeM.objects.filter(snippet_id=snippet_id).count()