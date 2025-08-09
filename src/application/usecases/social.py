import secrets
from src.application.security import Principal
from src.domain.entities import Comment, Like, SharedSnippet
from src.domain.policies import CommentPolicy, LikePolicy, SharePolicy
from src.domain.repositories.comment import CommentRepository
from src.domain.repositories.like import LikeRepository
from src.domain.repositories.snippet import SnippetRepository
from src.domain.repositories.share import SharedSnippetRepository
from datetime import datetime, timedelta


class SocialUseCase:
    def __init__(
        self,
        *,
        comment_repo: CommentRepository,
        like_repo: LikeRepository,
        snippet_repo: SnippetRepository,
        shared_snippet_repo: SharedSnippetRepository,
        comment_policy: CommentPolicy,
        like_policy: LikePolicy,
        share_policy: SharePolicy,
    ):
        self.comment_repo = comment_repo
        self.like_repo = like_repo
        self.snippet_repo = snippet_repo
        self.shared_snippet_repo = shared_snippet_repo
        self.comment_policy = comment_policy
        self.like_policy = like_policy
        self.share_policy = share_policy

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

    def share_snippet(
        self,
        principal: Principal,
        *,
        snippet_id: int,
        expires_in_hours: int = 24,
    ) -> str:
        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        user = principal.user
        snippet = self.snippet_repo.get_snippet_by_id(snippet_id)

        if not self.share_policy.can_share(user, snippet):
            raise Exception("User is not allowed to share this snippet")

        shared_snippet = SharedSnippet(
            snippet=snippet,
            created_by=user,
            is_active=True,
            token=secrets.token_urlsafe(12),
            expires_at=datetime.utcnow() + timedelta(hours=expires_in_hours),
        )
        self.shared_snippet_repo.create(shared_snippet)
        return shared_snippet.token

    def get_shared_snippet(
        self,
        principal: Principal,
        *,
        token: str,
    ) -> SharedSnippet:
        shared_snippet = self.shared_snippet_repo.get_by_token(token)

        if not shared_snippet or not shared_snippet.is_valid:
            raise Exception("Share link is invalid or expired")

        return shared_snippet
