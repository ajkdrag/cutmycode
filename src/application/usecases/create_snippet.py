from dataclasses import dataclass
from src.domain.entities import Snippet, SnippetDraft
from src.domain.ports.repositories import SnippetRepository
from src.application.security import Principal
from src.domain.policies import SnippetPolicy
from src.domain.constants import Language


@dataclass(frozen=True)
class CreateSnippetRequest:
    principal: Principal
    title: str
    description: str | None
    code: str
    language: Language
    is_public: bool


@dataclass(frozen=True)
class CreateSnippetResponse:
    snippet: Snippet


class CreateSnippet:
    def __init__(
        self,
        snippet_repo: SnippetRepository,
        snippet_policy: SnippetPolicy,
    ):
        self.snippet_repo = snippet_repo
        self.snippet_policy = snippet_policy

    def execute(
        self,
        request: CreateSnippetRequest,
    ) -> CreateSnippetResponse:
        principal = request.principal
        user = principal.user

        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        if not self.snippet_policy.can_create(user):
            raise Exception("User is not allowed to create snippets")

        draft = SnippetDraft(
            author_id=user.id,
            title=request.title,
            description=request.description,
            code=request.code,
            language=request.language,
            is_public=request.is_public,
        )
        snippet = self.snippet_repo.add(draft)
        return CreateSnippetResponse(snippet)
