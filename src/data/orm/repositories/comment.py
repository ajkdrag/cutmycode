from typing import List, Dict
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository

from src.domain.repositories.comment import CommentRepository
from src.data.orm.models import Comment as CommentModel
from src.domain.entities import Comment
from django.db.models import Count


class DjangoCommentRepository(CommentRepository):
    @staticmethod
    def _from_orm(comment_model: CommentModel) -> Comment:
        author_model = comment_model.author
        snippet_model = comment_model.snippet

        comment_author = DjangoUserRepository._from_orm(author_model)
        snippet = DjangoSnippetRepository._from_orm(snippet_model)

        return Comment(
            id=comment_model.id,
            body=comment_model.body,
            author=comment_author,
            snippet=snippet,
            is_deleted=comment_model.is_deleted,
            created_at=comment_model.created_at,
            updated_at=comment_model.updated_at,
        )

    def get(self, id: int) -> Comment:
        comment_model = CommentModel.objects.select_related(
            "author",
            "snippet__author",
        ).get(id=id)
        return self._from_orm(comment_model)

    def create(self, comment: Comment):
        comment_model = CommentModel(
            body=comment.body,
            author_id=comment.author.id,
            snippet_id=comment.snippet.id,
            is_deleted=comment.is_deleted,
        )
        comment_model.full_clean()
        comment_model.save()

    def update(self, comment: Comment):
        comment_model = CommentModel.objects.get(id=comment.id)
        comment_model.body = comment.body
        comment_model.is_deleted = comment.is_deleted
        comment_model.full_clean()
        comment_model.save()

    def delete(self, id: int) -> bool:
        try:
            comment_model = CommentModel.objects.get(id=id)
            comment_model.delete()
            return True
        except CommentModel.DoesNotExist:
            return False

    def get_comments_for_snippet(self, snippet_id: int) -> List[Comment]:
        comments = CommentModel.objects.select_related(
            "author", "snippet__author"
        ).filter(snippet_id=snippet_id, is_deleted=False)
        return [self._from_orm(comment_model) for comment_model in comments]

    def get_comment_counts_for_snippets(self, snippet_ids: List[int]) -> Dict[int, int]:
        """Get comment counts for multiple snippets in bulk."""
        comment_counts = (
            CommentModel.objects.filter(snippet_id__in=snippet_ids, is_deleted=False)
            .values("snippet_id")
            .annotate(count=Count("id"))
            .values_list("snippet_id", "count")
        )

        # Convert to dict with default 0 for snippets with no comments
        result = {snippet_id: 0 for snippet_id in snippet_ids}
        result.update(dict(comment_counts))
        return result
