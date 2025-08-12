from src.domain.types import UserId
from src.data.orm.models import CustomUser as CustomUserM
from src.domain.entities import User


class DjangoUserRepository:
    @staticmethod
    def _from_orm(user_model: CustomUserM) -> User:
        return User(
            id=UserId(user_model.id),
            username=user_model.username,
            email=user_model.email,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            about=user_model.about,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

    def get(self, user_id: UserId) -> User | None:
        try:
            user_model = CustomUserM.objects.get(id=user_id)
            return self._from_orm(user_model)
        except CustomUserM.DoesNotExist:
            return None
