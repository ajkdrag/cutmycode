# poor man's DI
from src.data.orm.repositories.snippet import DjangoSnippetRepository
from src.data.orm.repositories.user import DjangoUserRepository
from src.data.orm.repositories.like import DjangoLikeRepository
from src.data.orm.repositories.comment import DjangoCommentRepository
from src.data.orm.repositories.share import DjangoSnippetShareLinkRepository
from src.domain.policies import (
    SnippetPolicy,
    CommentPolicy,
    LikePolicy,
    SharePolicy,
)
from src.data.orm.queries import DjangoSnippetsReadModel

from src.application.usecases.create_snippet import CreateSnippet
from src.application.usecases.update_snippet import UpdateSnippet
from src.application.usecases.get_snippet_details import GetSnippetDetails
from src.application.usecases.get_author_details import GetAuthorDetails
from src.application.usecases.get_author_snippet_previews import GetAuthorSnippets
from src.application.usecases.get_public_snippet_previews import GetPublicSnippets
from src.application.usecases.get_user_snippet_previews import GetUserSnippets
from src.application.usecases.toggle_like import ToggleLike
from src.application.usecases.create_comment import CreateComment
from src.application.usecases.create_share_link import CreateShareLink
from src.application.usecases.view_shared_snippet import ViewSharedSnippet
from src.application.usecases.get_search_results import GetSearchResults

from src.application.security import Principal

snippet_repo = DjangoSnippetRepository()
user_repo = DjangoUserRepository()
like_repo = DjangoLikeRepository()
comment_repo = DjangoCommentRepository()
share_link_repo = DjangoSnippetShareLinkRepository()
read_model = DjangoSnippetsReadModel()

snippet_policy = SnippetPolicy()
comment_policy = CommentPolicy()
like_policy = LikePolicy()
share_policy = SharePolicy()

create_snippet_uc = CreateSnippet(
    snippet_repo=snippet_repo,
    snippet_policy=snippet_policy,
)
update_snippet_uc = UpdateSnippet(
    snippet_repo=snippet_repo,
    snippet_policy=snippet_policy,
)
get_snippet_details_uc = GetSnippetDetails(
    read_model=read_model,
    comment_repo=comment_repo,
    snippet_policy=snippet_policy,
)
get_author_details_uc = GetAuthorDetails(
    user_repo=user_repo,
    read_model=snippet_repo,
)
get_author_snippets_uc = GetAuthorSnippets(
    read_model=read_model,
)
get_public_snippets_uc = GetPublicSnippets(
    read_model=read_model,
)
get_user_snippets_uc = GetUserSnippets(
    read_model=read_model,
)
toggle_like_uc = ToggleLike(
    like_repo=like_repo,
    snippet_repo=snippet_repo,
    like_policy=like_policy,
)
create_comment_uc = CreateComment(
    comment_repo=comment_repo,
    snippet_repo=snippet_repo,
    comment_policy=comment_policy,
    snippet_policy=snippet_policy,
)
get_search_results_uc = GetSearchResults(
    read_model=read_model,
)
create_share_link_uc = CreateShareLink(
    snippet_repo=snippet_repo,
    share_link_repo=share_link_repo,
    snippet_policy=snippet_policy,
    share_policy=share_policy,
)
view_shared_snippet_uc = ViewSharedSnippet(
    snippet_repo=snippet_repo,
    share_link_repo=share_link_repo,
)


def get_principal(request):
    if request.user.is_authenticated:
        user = user_repo._from_orm(request.user)
        return Principal.authenticated(user)
    return Principal.anonymous()
