from src.domain.repositories.comment import CommentRepository
from src.domain.repositories.like import LikeRepository
from src.domain.repositories.snippet import SnippetRepository
from src.domain.repositories.user import UserRepository
from src.domain.policies import SnippetPolicy, UserInteractionPolicy
from src.domain.entities import Snippet
from src.domain.value_objects import (
    SnippetWithMetadata,
    UserSnippetInteractions,
    SnippetMetadata,
    SnippetStats,
)
from src.application.security import Principal
from src.application.dtos import UserDetailDTO
from typing import List


class UsersUseCase:
    def __init__(
        self,
        *,
        user_repo: UserRepository,
        snippet_repo: SnippetRepository,
        like_repo: LikeRepository,
        comment_repo: CommentRepository,
        snippet_policy: SnippetPolicy,
        user_interaction_policy: UserInteractionPolicy,
    ):
        self.user_repo = user_repo
        self.snippet_repo = snippet_repo
        self.like_repo = like_repo
        self.comment_repo = comment_repo
        self.snippet_policy = snippet_policy
        self.user_interaction_policy = user_interaction_policy

    def _enrich_snippets_with_stats(
        self,
        principal: Principal,
        *,
        snippets: List[Snippet],
    ) -> List[SnippetWithMetadata]:
        snippet_ids = [snippet.id for snippet in snippets]
        count_like = self.like_repo.get_like_counts_for_snippets(
            snippet_ids,
        )
        count_comment = self.comment_repo.get_comment_counts_for_snippets(
            snippet_ids,
        )

        user_interactions = {}
        if principal.is_authenticated:
            like_status = self.like_repo.get_like_status_for_snippets(
                principal.user.id,
                snippet_ids,
            )
            user_interactions = {
                snippet_id: UserSnippetInteractions(
                    liked=like_status.get(snippet_id, False),
                    commented=False,
                )
                for snippet_id in snippet_ids
            }

        snippets = [
            SnippetWithMetadata(
                **snippet.__dict__,
                metadata=SnippetMetadata(
                    stats=SnippetStats(
                        like_count=count_like.get(snippet.id, 0),
                        comment_count=count_comment.get(snippet.id, 0),
                    ),
                    interactions=user_interactions.get(snippet.id),
                ),
            )
            for snippet in snippets
        ]

        return snippets

    def get_user_detail(
        self,
        principal: Principal,
        *,
        user_id: int,
        with_meta: bool = True,
    ) -> UserDetailDTO:
        user = principal.user
        snippets = self.snippet_repo.get_user_snippets(
            user_id,
            only_public=True,
        )

        if self.user_interaction_policy.can_view_private(user, user_id):
            snippets += self.snippet_repo.get_user_private_snippets(user_id)

        if with_meta:
            snippets = self._enrich_snippets_with_stats(
                principal,
                snippets=snippets,
            )

        return UserDetailDTO(
            user=self.user_repo.get(user_id),
            snippets=snippets,
        )
