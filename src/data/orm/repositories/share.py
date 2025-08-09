from typing import Optional

from datetime import datetime
from src.data.orm.models import SharedSnippet as SharedSnippetModel
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.domain.entities import SharedSnippet
from src.domain.repositories.share import SharedSnippetRepository


class DjangoSharedSnippetRepository(SharedSnippetRepository):
    @staticmethod
    def _from_orm(share_model: SharedSnippetModel) -> SharedSnippet:
        snippet_model = share_model.snippet
        created_by_model = share_model.created_by
        snippet = DjangoSnippetRepository._from_orm(snippet_model)
        created_by = DjangoUserRepository._from_orm(created_by_model)

        return SharedSnippet(
            id=share_model.id,
            snippet=snippet,
            token=share_model.token,
            expires_at=share_model.expires_at,
            is_active=share_model.is_active,
            created_by=created_by,
            created_at=share_model.created_at,
            updated_at=share_model.updated_at,
        )

    def get(self, id: int) -> SharedSnippet:
        pass

    def create(self, share: SharedSnippet):
        share_model = SharedSnippetModel(
            snippet_id=share.snippet.id,
            token=share.token,
            expires_at=share.expires_at,
            created_by_id=share.created_by.id,
        )

        share_model.full_clean()
        share_model.save()

    def update(self, share: SharedSnippet):
        pass

    def delete(self, id: int) -> bool:
        pass

    def get_by_token(self, token: str) -> Optional[SharedSnippet]:
        try:
            share_model = SharedSnippetModel.objects.get(token=token)
            return self._from_orm(share_model)
        except SharedSnippetModel.DoesNotExist:
            return None

    def deactivate_expired_shares(self) -> None:
        # during creation utcnow() was used, so using it here as well
        SharedSnippetModel.objects.filter(
            expires_at__lte=datetime.utcnow(),
        ).update(is_active=False)
