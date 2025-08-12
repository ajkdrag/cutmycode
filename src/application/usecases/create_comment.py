from dataclasses import dataclass
from src.domain.types import SnippetId
from src.domain.entities import Comment, CommentDraft
from src.domain.ports.repositories import CommentRepository, SnippetRepository
from src.application.security import Principal
from src.domain.policies import CommentPolicy, SnippetPolicy


@dataclass(frozen=True)
class CreateCommentRequest:
    principal: Principal
    snippet_id: int
    body: str


@dataclass(frozen=True)
class CreateCommentResponse:
    comment: Comment


class CreateComment:
    def __init__(
        self,
        comment_repo: CommentRepository,
        snippet_repo: SnippetRepository,
        comment_policy: CommentPolicy,
        snippet_policy: SnippetPolicy,
    ):
        self.comment_repo = comment_repo
        self.snippet_repo = snippet_repo
        self.comment_policy = comment_policy
        self.snippet_policy = snippet_policy

    def execute(
        self,
        request: CreateCommentRequest,
    ) -> CreateCommentResponse:
        principal = request.principal
        user = principal.user
        snippet_id = SnippetId(request.snippet_id)

        if not principal.is_authenticated:
            raise Exception("User is not authenticated")

        snippet = self.snippet_repo.get(snippet_id)
        if not snippet:
            raise Exception("Snippet not found")

        if not self.comment_policy.can_create(user, snippet):
            raise Exception("User is not allowed to comment on snippets")

        if not request.body or not request.body.strip():
            raise Exception("Comment body cannot be empty")

        draft = CommentDraft(
            author_id=user.id,
            snippet_id=snippet_id,
            body=request.body.strip(),
        )
        comment = self.comment_repo.add(draft)
        return CreateCommentResponse(comment=comment)

