from typing import List
from src.domain.entities import Snippet
from src.domain.repositories.like import LikeRepository
from src.domain.repositories.comment import CommentRepository
from src.domain.value_objects import SnippetWithMetadata
from src.application.security import Principal


def enrich_snippets_with_stats(
    principal: Principal,
    *,
    snippets: List[Snippet],
    like_repo: LikeRepository,
    comment_repo: CommentRepository,
) -> List[SnippetWithMetadata]:
    snippet_ids = [snippet.id for snippet in snippets]
    count_like = like_repo.get_like_counts_for_snippets(
        snippet_ids,
    )
    count_comment = comment_repo.get_comment_counts_for_snippets(
        snippet_ids,
    )

    user_interactions = {}
    if principal.is_authenticated:
        like_status = like_repo.get_like_status_for_snippets(
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
            snippet=snippet,
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
