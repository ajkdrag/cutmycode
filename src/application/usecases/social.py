from src.application.security import Principal
from src.domain.entities import Comment, Like
from src.domain.policies import CommentPolicy, LikePolicy
from src.domain.repositories.comment import CommentRepository
from src.domain.repositories.like import LikeRepository
from src.domain.repositories.snippet import SnippetRepository


class SocialUseCase:
    def __init__(
        self,
        *,
        comment_repo: CommentRepository,
        like_repo: LikeRepository,
        snippet_repo: SnippetRepository,
        comment_policy: CommentPolicy,
        like_policy: LikePolicy,
    ):
        self.comment_repo = comment_repo
        self.like_repo = like_repo
        self.snippet_repo = snippet_repo
        self.comment_policy = comment_policy
        self.like_policy = like_policy

    def create_comment(
        self,
        principal: Principal,
        *,
        body: str,
        snippet_id: int,
    ):
        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        user = principal.user
        snippet = self.snippet_repo.get_snippet_by_id(snippet_id)

        if not self.comment_policy.can_create(user, snippet):
            raise Exception("User is not allowed to comment on this snippet")

        comment = Comment(
            body=body,
            author=user,
            snippet=snippet,
            is_deleted=False,
        )

        return self.comment_repo.create(comment)

    def like_or_unlike_snippet(
        self,
        principal: Principal,
        *,
        snippet_id: int,
    ):
        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        user = principal.user
        snippet = self.snippet_repo.get_snippet_by_id(snippet_id)

        if not self.like_policy.can_like_or_unlike(user, snippet):
            raise Exception("User is not allowed to like this snippet")

        like = self.like_repo.get_like_if_exists(user.id, snippet_id)
        if like is not None:
            self.like_repo.unlike(like)
        else:
            self.like_repo.like(Like(user=user, snippet=snippet))
