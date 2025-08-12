from datetime import datetime, timezone
from src.domain.types import SnippetId, UserId, SnippetShareLinkId
from src.data.orm.models import SharedSnippet as SharedSnippetM
from src.domain.entities import SnippetShareLink, SnippetShareLinkDraft
from src.domain.value_objects import AuthorRef


class DjangoSnippetShareLinkRepository:
    @staticmethod
    def _from_orm(shared_snippet_model: SharedSnippetM) -> SnippetShareLink:
        return SnippetShareLink(
            id=SnippetShareLinkId(shared_snippet_model.id),
            snippet_id=SnippetId(shared_snippet_model.snippet.id),
            shared_by=AuthorRef(
                id=UserId(shared_snippet_model.shared_by.id),
                username=shared_snippet_model.shared_by.username,
            ),
            token=shared_snippet_model.token,
            expires_at=shared_snippet_model.expires_at,
            is_active=shared_snippet_model.is_active,
            created_at=shared_snippet_model.created_at,
            updated_at=shared_snippet_model.updated_at,
        )

    def add(self, draft: SnippetShareLinkDraft) -> SnippetShareLink:
        import secrets

        token = secrets.token_urlsafe(12)

        shared_snippet_model = SharedSnippetM(
            snippet_id=draft.snippet_id,
            shared_by_id=draft.shared_by_id,
            token=token,
            expires_at=draft.expires_at,
        )
        shared_snippet_model.full_clean()
        shared_snippet_model.save()
        return self._from_orm(shared_snippet_model)

    def get_by_token(self, token: str) -> SnippetShareLink | None:
        try:
            shared_snippet_model = SharedSnippetM.objects.select_related(
                "snippet", "shared_by"
            ).get(token=token)
            return self._from_orm(shared_snippet_model)
        except SharedSnippetM.DoesNotExist:
            return None

    def deactivate_expired(self) -> None:
        # using utc time here since expires_at was calculated in utc
        now = datetime.now(tz=timezone.utc)
        SharedSnippetM.objects.filter(
            expires_at__lt=now,
            is_active=True,
        ).update(is_active=False)

