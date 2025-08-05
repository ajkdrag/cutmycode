from src.application.security import Principal
from src.domain.policies import CommentPolicy
from src.data.orm.repositories.comment import DjangoCommentRepository
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.interfaces.web.forms.social import CommentForm


def handle_comment_on_snippet(
    request,
    *,
    snippet_id: int,
    comment_form: CommentForm,
    principal: Principal,
):
    """
    Precondition: form is valid (checked by caller)
    """
    if request.method != "POST":
        return
    if not request.user.is_authenticated:
        print("inside...")
        redirect_to_login(request)

    policy = CommentPolicy()
    comment_repo = DjangoCommentRepository()
    snippet_repo = DjangoSnippetRepository()

    create_comment(
        comment_repo=comment_repo,
        snippet_repo=snippet_repo,
        policy=policy,
        body=comment_form.cleaned_data["body"],
        principal=principal,
        snippet_id=snippet_id,
    )
