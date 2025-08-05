from src.domain.repositories.snippet import SnippetRepository
from src.data.orm.models import Snippet as SnippetModel
from src.domain.entities import Snippet, User
from src.domain.value_objects import SearchQuery, SearchResult
from typing import List
from django.db.models import Count, Q


class DjangoSnippetRepository(SnippetRepository):
    @staticmethod
    def _from_orm(snippet_model: SnippetModel) -> Snippet:
        author_model = snippet_model.author
        author = User(
            id=author_model.id,
            username=author_model.username,
            email=author_model.email,
            is_active=author_model.is_active,
            created_at=author_model.created_at,
            updated_at=author_model.updated_at,
        )

        return Snippet(
            id=snippet_model.id,
            title=snippet_model.title,
            code=snippet_model.code,
            description=snippet_model.description,
            language=snippet_model.language,
            is_public=snippet_model.is_public,
            author=author,
            created_at=snippet_model.created_at,
            updated_at=snippet_model.updated_at,
        )

    def get(self, id: int) -> Snippet:
        snippet_model = SnippetModel.objects.get(id=id)
        return self._from_orm(snippet_model)

    def create(self, snippet: Snippet) -> Snippet:
        snippet_model = SnippetModel(
            title=snippet.title,
            code=snippet.code,
            description=snippet.description,
            language=snippet.language,
            is_public=snippet.is_public,
            author_id=snippet.author.id,
        )
        snippet_model.full_clean()
        snippet_model.save()

    def update(self, snippet: Snippet) -> Snippet:
        snippet_model = SnippetModel.objects.get(id=snippet.id)
        snippet_model.title = snippet.title
        snippet_model.description = snippet.description
        snippet_model.code = snippet.code
        snippet_model.language = snippet.language
        snippet_model.is_public = snippet.is_public
        snippet_model.full_clean()
        snippet_model.save()

    def delete(self, id: int) -> bool:
        pass

    def get_public_snippets(self) -> List[Snippet]:
        snippets = SnippetModel.objects.filter(is_public=True)
        return [self._from_orm(snippet_model) for snippet_model in snippets]

    def get_user_snippets(self, user_id: int) -> List[Snippet]:
        snippets = SnippetModel.objects.filter(author_id=user_id)
        return [self._from_orm(snippet_model) for snippet_model in snippets]

    def get_user_private_snippets(self, user_id: int) -> List[Snippet]:
        snippets = SnippetModel.objects.filter(
            author_id=user_id,
            is_public=False,
        )
        return [self._from_orm(snippet_model) for snippet_model in snippets]

    def get_snippet_by_id(self, snippet_id: int) -> Snippet:
        snippet_model = SnippetModel.objects.get(id=snippet_id)
        return self._from_orm(snippet_model)

    def get_visible_snippets(self, user_id: int) -> List[Snippet]:
        snippets = SnippetModel.objects.filter(
            Q(is_public=True) | Q(author_id=user_id),
        )
        return [self._from_orm(snippet_model) for snippet_model in snippets]

    def _build_search_queryset(
        self,
        search_query: SearchQuery,
        is_public_only: bool = True,
        user_id: int = None,
    ):
        """Build queryset for search with filters."""
        queryset = SnippetModel.objects.all()

        if is_public_only:
            queryset = queryset.filter(is_public=True)
        elif user_id is not None:
            queryset = queryset.filter(Q(is_public=True) | Q(author_id=user_id))

        if search_query.query.strip():
            search_q = Q(title__icontains=search_query.query) | Q(
                description__icontains=search_query.query
            )
            queryset = queryset.filter(search_q)

        if search_query.language:
            queryset = queryset.filter(language=search_query.language)

        return (
            queryset.annotate(
                like_count=Count("likes", distinct=True),
                comment_count=Count("comments", distinct=True),
            )
            .select_related("author")
            .order_by("-created_at")
        )

    def search_across_public_snippets(self, search_query: SearchQuery) -> SearchResult:
        queryset = self._build_search_queryset(
            search_query,
            is_public_only=True,
        )

        snippets = [self._from_orm(snippet_model) for snippet_model in queryset]

        return SearchResult(snippets=snippets)

    def search_across_visible_snippets(
        self, search_query: SearchQuery, user_id: int
    ) -> SearchResult:
        """Search all snippets accessible to user (public + own private) with pagination and filters."""
        queryset = self._build_search_queryset(
            search_query, is_public_only=False, user_id=user_id
        )
        snippets = [self._from_orm(snippet_model) for snippet_model in queryset]

        return SearchResult(snippets=snippets)
