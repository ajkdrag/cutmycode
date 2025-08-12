from typing import List
from src.domain.types import UserId, SnippetId, CommentId
from src.data.orm.models import Comment as CommentM
from src.domain.entities import Comment, CommentDraft
from src.domain.value_objects import AuthorRef


class DjangoCommentRepository:
    @staticmethod
    def _from_orm(comment_model: CommentM) -> Comment:
        return Comment(
            id=CommentId(comment_model.id),
            author=AuthorRef(
                id=UserId(comment_model.author.id),
                username=comment_model.author.username,
            ),
            snippet_id=SnippetId(comment_model.snippet.id),
            body=comment_model.body,
            is_deleted=comment_model.is_deleted,
            created_at=comment_model.created_at,
            updated_at=comment_model.updated_at,
        )

    def add(self, draft: CommentDraft) -> Comment:
        comment_model = CommentM(
            author_id=draft.author_id,
            snippet_id=draft.snippet_id,
            body=draft.body,
        )
        comment_model.full_clean()
        comment_model.save()
        return self._from_orm(comment_model)

    def get(self, comment_id: CommentId) -> Comment | None:
        try:
            comment_model = CommentM.objects.select_related(
                "author",
                "snippet",
            ).get(id=comment_id)
            return self._from_orm(comment_model)
        except CommentM.DoesNotExist:
            return None

    def update(self, comment: Comment) -> None:
        CommentM.objects.filter(id=comment.id).update(
            body=comment.body,
            is_deleted=comment.is_deleted,
        )

    def list_for_snippet(self, snippet_id: SnippetId) -> List[Comment]:
        comment_models = (
            CommentM.objects.select_related("author", "snippet")
            .filter(snippet_id=snippet_id, is_deleted=False)
            .order_by("-created_at")
        )
        return [self._from_orm(comment_model) for comment_model in comment_models]

    def list_for_user(self, user_id: UserId) -> List[Comment]:
        comment_models = (
            CommentM.objects.select_related("author", "snippet")
            .filter(author_id=user_id, is_deleted=False)
            .order_by("-created_at")
        )
        return [self._from_orm(comment_model) for comment_model in comment_models]

