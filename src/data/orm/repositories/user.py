from typing import Optional
from src.domain.repositories.user import UserRepository
from src.data.orm.models import CustomUser as CustomUserModel
from src.domain.entities import User, AnonymousUser


class DjangoUserRepository(UserRepository):
    @staticmethod
    def _from_orm(user_model: CustomUserModel) -> User:
        if user_model.is_anonymous:
            return AnonymousUser()
        return User(
            id=user_model.id,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            about=user_model.about,
            username=user_model.username,
            email=user_model.email,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )

    def get(self, id: Optional[int]) -> User:
        if id is None:
            return AnonymousUser()
        user_model = CustomUserModel.objects.get(id=id)
        return self._from_orm(user_model)

    def create(self, user: User) -> User:
        user_model = CustomUserModel(
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )
        user_model.full_clean()
        user_model.save()

    def update(self, user: User) -> User:
        pass

    def delete(self, id: int) -> bool:
        pass
