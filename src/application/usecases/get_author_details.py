from dataclasses import dataclass
from src.domain.types import UserId
from src.domain.entities import User
from src.domain.ports.queries import SnippetsReadModel
from src.domain.ports.repositories import UserRepository
from src.application.security import Principal


@dataclass(frozen=True)
class GetAuthorDetailsRequest:
    principal: Principal
    author_id: int


@dataclass(frozen=True)
class GetAuthorDetailsResponse:
    author: User


class GetAuthorDetails:
    def __init__(
        self,
        user_repo: UserRepository,
        read_model: SnippetsReadModel,
    ):
        self.user_repo = user_repo
        self.read_model = read_model

    def execute(
        self,
        request: GetAuthorDetailsRequest,
    ) -> GetAuthorDetailsResponse:
        author_id = UserId(request.author_id)
        author = self.user_repo.get(author_id)
        return GetAuthorDetailsResponse(author=author)
