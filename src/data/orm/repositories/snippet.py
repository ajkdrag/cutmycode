from src.domain.types import SnippetId
from src.data.orm.models import Snippet as SnippetM
from src.domain.entities import Snippet, SnippetDraft
from src.domain.value_objects import AuthorRef
from src.domain.constants import Language


class DjangoSnippetRepository:
    @staticmethod
    def _from_orm(snippet_model: SnippetM) -> Snippet:
        return Snippet(
            id=SnippetId(snippet_model.id),
            author=AuthorRef(
                id=snippet_model.author.id,
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

    def get(self, snippet_id: SnippetId) -> Snippet | None:
        try:
            snippet_model = SnippetM.objects.get(id=snippet_id)
            return self._from_orm(snippet_model)
        except SnippetM.DoesNotExist:
            return None

    def add(self, draft: SnippetDraft) -> Snippet:
        snippet_model = SnippetM(
            author_id=draft.author_id,
            title=draft.title,
            description=draft.description,
            code=draft.code,
            language=draft.language.name,
            is_public=draft.is_public,
        )
        snippet_model.full_clean()
        snippet_model.save()
        return self._from_orm(snippet_model)

    def update(self, snippet_id: SnippetId, draft: SnippetDraft) -> Snippet:
        snippet_model = SnippetM.objects.get(id=snippet_id)
        snippet_model.title = draft.title
        snippet_model.description = draft.description
        snippet_model.code = draft.code
        snippet_model.language = draft.language.name
        snippet_model.is_public = draft.is_public
        snippet_model.full_clean()
        snippet_model.save()
        return self._from_orm(snippet_model)
