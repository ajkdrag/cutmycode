from dataclasses import dataclass
from src.domain.types import SnippetId
from src.domain.entities import Snippet, SnippetDraft
from src.domain.ports.repositories import SnippetRepository
from src.application.security import Principal
from src.domain.policies import SnippetPolicy
from src.domain.constants import Language


@dataclass(frozen=True)
class UpdateSnippetRequest:
    principal: Principal
    snippet_id: int
    title: str
    description: str
    code: str
    language: Language
    is_public: bool


@dataclass(frozen=True)
class UpdateSnippetResponse:
    snippet: Snippet


class UpdateSnippet:
    def __init__(
        self,
        snippet_repo: SnippetRepository,
        snippet_policy: SnippetPolicy,
    ):
        self.snippet_repo = snippet_repo
        self.snippet_policy = snippet_policy

    def execute(
        self,
        request: UpdateSnippetRequest,
    ) -> UpdateSnippetResponse:
        principal = request.principal
        user = principal.user
        snippet_id = SnippetId(request.snippet_id)

        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        snippet = self.snippet_repo.get(snippet_id)

        if not self.snippet_policy.can_edit(user, snippet):
            raise Exception("User is not allowed to edit this snippet")

        snippet = self.snippet_repo.update(
            snippet_id,
            SnippetDraft(
                author_id=snippet.author.id,
                title=request.title,
                description=request.description,
                code=request.code,
                language=request.language,
                is_public=request.is_public,
            ),
        )

        return UpdateSnippetResponse(snippet)
