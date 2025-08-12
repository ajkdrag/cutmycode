from typing import List
from django.db.models import Count, Exists, OuterRef, Q
from src.domain.types import UserId, SnippetId
from src.domain.dtos import SnippetWithMetadata
from src.domain.entities import Snippet
from src.domain.value_objects import (
    AuthorRef,
    SnippetStats,
    UserSnippetInteractions,
    SnippetMetadata,
)
from src.domain.constants import Language
from src.data.orm.models import Snippet as SnippetM, Like as LikeM, Comment as CommentM


class DjangoSnippetsReadModel:
    @staticmethod
    def _from_orm_with_metadata(
        snippet_model: SnippetM, user_id: UserId | None = None
    ) -> SnippetWithMetadata:
        snippet = Snippet(
            id=SnippetId(snippet_model.id),
            author=AuthorRef(
                id=UserId(snippet_model.author.id),
                username=snippet_model.author.username,
            ),
            title=snippet_model.title,
            code=snippet_model.code,
            description=snippet_model.description,
            language=Language[snippet_model.language],
            is_public=snippet_model.is_public,
            created_at=snippet_model.created_at,
            updated_at=snippet_model.updated_at,
        )

        # Build metadata with stats and user interactions if user_id provided
        stats = SnippetStats(
            like_count=getattr(snippet_model, "like_count", 0),
            comment_count=getattr(snippet_model, "comment_count", 0),
        )

        interactions = None
        if user_id is not None:
            interactions = UserSnippetInteractions(
                liked=getattr(snippet_model, "user_liked", False),
                commented=getattr(snippet_model, "user_commented", False),
            )

        metadata = SnippetMetadata(stats=stats, interactions=interactions)

        return SnippetWithMetadata(
            id=snippet.id,
            author=snippet.author,
            title=snippet.title,
            code=snippet.code,
            description=snippet.description,
            language=snippet.language,
            is_public=snippet.is_public,
            created_at=snippet.created_at,
            updated_at=snippet.updated_at,
            metadata=metadata,
        )

    def get_with_meta(
        self, snippet_id: SnippetId, user_id: UserId | None = None
    ) -> SnippetWithMetadata:
        queryset = SnippetM.objects.select_related("author").annotate(
            like_count=Count("likes", distinct=True),
            comment_count=Count(
                "comments",
                filter=Q(comments__is_deleted=False),
                distinct=True,
            ),
        )

        if user_id is not None:
            queryset = queryset.annotate(
                user_liked=Exists(
                    LikeM.objects.filter(
                        snippet=OuterRef("pk"),
                        user_id=user_id,
                    )
                ),
                user_commented=Exists(
                    CommentM.objects.filter(
                        snippet=OuterRef("pk"),
                        author_id=user_id,
                        is_deleted=False,
                    )
                ),
            )

        snippet_model = queryset.get(id=snippet_id)
        return self._from_orm_with_metadata(snippet_model, user_id)

    def list_public_with_meta(
        self, user_id: UserId | None = None, limit: int = 10, offset: int = 0
    ) -> List[SnippetWithMetadata]:
        queryset = (
            SnippetM.objects.select_related("author")
            .filter(is_public=True)
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count(
                    "comments",
                    filter=Q(comments__is_deleted=False),
                    distinct=True,
                ),
            )
        )

        if user_id is not None:
            queryset = queryset.annotate(
                user_liked=Exists(
                    LikeM.objects.filter(
                        snippet=OuterRef("pk"),
                        user_id=user_id,
                    )
                ),
                user_commented=Exists(
                    CommentM.objects.filter(
                        snippet=OuterRef("pk"),
                        author_id=user_id,
                        is_deleted=False,
                    )
                ),
            )

        snippet_models = queryset.order_by("-created_at")[offset : offset + limit]
        return [
            self._from_orm_with_metadata(snippet_model, user_id)
            for snippet_model in snippet_models
        ]

    def list_from_author_with_meta(
        self,
        author_id: UserId,
        user_id: UserId | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[SnippetWithMetadata]:
        """Public snippets from author"""
        queryset = (
            SnippetM.objects.select_related("author")
            .filter(author_id=author_id, is_public=True)
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count(
                    "comments",
                    filter=Q(comments__is_deleted=False),
                    distinct=True,
                ),
            )
        )

        if user_id is not None:
            queryset = queryset.annotate(
                user_liked=Exists(
                    LikeM.objects.filter(
                        snippet=OuterRef("pk"),
                        user_id=user_id,
                    )
                ),
                user_commented=Exists(
                    CommentM.objects.filter(
                        snippet=OuterRef("pk"),
                        author_id=user_id,
                        is_deleted=False,
                    )
                ),
            )

        snippet_models = queryset.order_by("-created_at")[offset : offset + limit]
        return [
            self._from_orm_with_metadata(snippet_model, user_id)
            for snippet_model in snippet_models
        ]

    def list_from_user_with_meta(
        self,
        user_id: UserId,
        limit: int = 10,
        offset: int = 0,
    ) -> List[SnippetWithMetadata]:
        """Snippets from user (public + private)"""
        queryset = (
            SnippetM.objects.select_related("author")
            .filter(author_id=user_id)
            .annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count(
                    "comments",
                    filter=Q(comments__is_deleted=False),
                    distinct=True,
                ),
                # For this method, we include user interactions for the owner themselves
                user_liked=Exists(
                    LikeM.objects.filter(
                        snippet=OuterRef("pk"),
                        user_id=user_id,
                    )
                ),
                user_commented=Exists(
                    CommentM.objects.filter(
                        snippet=OuterRef("pk"),
                        author_id=user_id,
                        is_deleted=False,
                    )
                ),
            )
        )

        snippet_models = queryset.order_by("-created_at")[offset : offset + limit]
        return [
            self._from_orm_with_metadata(snippet_model, user_id)
            for snippet_model in snippet_models
        ]

    def search_snippets(
        self,
        search_text: str,
        language: str | None = None,
        user_id: UserId | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> List[SnippetWithMetadata]:
        queryset = SnippetM.objects.select_related("author").filter(
            Q(title__icontains=search_text) | Q(description__icontains=search_text),
            is_public=True,
        )

        if language is not None:
            queryset = queryset.filter(language=language)

        queryset = queryset.annotate(
            like_count=Count("likes", distinct=True),
            comment_count=Count(
                "comments",
                filter=Q(comments__is_deleted=False),
                distinct=True,
            ),
        )

        if user_id is not None:
            queryset = queryset.annotate(
                user_liked=Exists(
                    LikeM.objects.filter(
                        snippet=OuterRef("pk"),
                        user_id=user_id,
                    )
                ),
                user_commented=Exists(
                    CommentM.objects.filter(
                        snippet=OuterRef("pk"),
                        author_id=user_id,
                        is_deleted=False,
                    )
                ),
            )

        snippet_models = queryset.order_by("-created_at")[offset : offset + limit]
        return [
            self._from_orm_with_metadata(snippet_model, user_id)
            for snippet_model in snippet_models
        ]
