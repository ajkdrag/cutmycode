from typing import List
from src.application.dtos import (
    ListSnippetsDTO,
    SearchResultsDTO,
    SnippetDetailDTO,
)
from src.application.security import Principal
from src.domain.entities import Snippet
from src.domain.policies import SnippetPolicy
from src.domain.repositories.comment import CommentRepository
from src.domain.repositories.like import LikeRepository
from src.domain.repositories.snippet import SnippetRepository
from src.domain.value_objects import (
    SearchQuery,
    SnippetMetadata,
    SnippetStats,
    SnippetWithMetadata,
    UserSnippetInteractions,
)


class SnippetsUseCase:
    def __init__(
        self,
        *,
        snippet_repo: SnippetRepository,
        like_repo: LikeRepository,
        comment_repo: CommentRepository,
        snippet_policy: SnippetPolicy,
    ):
        self.snippet_repo = snippet_repo
        self.like_repo = like_repo
        self.comment_repo = comment_repo
        self.snippet_policy = snippet_policy

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

    def create_snippet(
        self,
        principal: Principal,
        *,
        title: str,
        description: str,
        code: str,
        language: str,
        is_public: bool,
    ):
        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        user = principal.user
        if not self.snippet_policy.can_create(user):
            raise Exception("User is not allowed to create snippets")

        snippet = Snippet(
            title=title,
            description=description,
            code=code,
            language=language,
            is_public=is_public,
            author=user,
        )

        self.snippet_repo.create(snippet)

    def update_snippet(
        self,
        principal: Principal,
        *,
        snippet_id: int,
        title: str,
        description: str,
        code: str,
        language: str,
        is_public: bool,
    ):
        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        user = principal.user
        snippet = self.snippet_repo.get_snippet_by_id(snippet_id)

        if not self.snippet_policy.can_edit(user, snippet):
            raise Exception("User is not allowed to edit this snippet")

        snippet.title = title
        snippet.description = description
        snippet.code = code
        snippet.language = language
        snippet.is_public = is_public

        self.snippet_repo.update(snippet)

    def get_visible_snippets(
        self,
        principal: Principal,
        *,
        with_meta: bool = True,
    ) -> ListSnippetsDTO:
        snippets = self.snippet_repo.get_public_snippets()
        if principal.is_authenticated:
            snippets += self.snippet_repo.get_user_private_snippets(
                principal.user.id,
            )

        if with_meta:
            snippets = self._enrich_snippets_with_stats(
                principal,
                snippets=snippets,
            )

        return ListSnippetsDTO(snippets=snippets)

    def get_snippet_detail(
        self,
        principal: Principal,
        *,
        snippet_id: int,
        with_meta: bool = True,
    ) -> SnippetDetailDTO:
        user = principal.user
        snippet = self.snippet_repo.get_snippet_by_id(snippet_id)

        if not self.snippet_policy.can_view(user, snippet):
            raise Exception("User is not allowed to view this snippet")

        if with_meta:
            snippet = self._enrich_snippets_with_stats(
                principal,
                snippets=[snippet],
            )[0]

        comments = self.comment_repo.get_comments_for_snippet(snippet_id)
        return SnippetDetailDTO(
            snippet=snippet,
            comments=comments,
        )

    def get_user_snippets(
        self,
        principal: Principal,
        *,
        with_meta: bool = True,
    ) -> ListSnippetsDTO:
        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        snippets = self.snippet_repo.get_user_snippets(principal.user.id)
        if with_meta:
            snippets = self._enrich_snippets_with_stats(
                principal,
                snippets=snippets,
            )

        return ListSnippetsDTO(snippets=snippets)

    def search_snippets(
        self,
        principal: Principal,
        *,
        search_query: SearchQuery,
        with_meta: bool = True,
    ) -> SearchResultsDTO:
        if principal.is_authenticated:
            search_result = self.snippet_repo.search_across_visible_snippets(
                search_query, principal.user.id
            )
        else:
            search_result = self.snippet_repo.search_across_public_snippets(
                search_query
            )

        snippets = search_result.snippets
        if with_meta:
            snippets = self._enrich_snippets_with_stats(
                principal,
                snippets=search_result.snippets,
            )

        return SearchResultsDTO(
            snippets=snippets,
            query=search_query.query,
        )
