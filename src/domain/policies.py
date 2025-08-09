from src.domain.entities import Snippet, User, AnonymousUser, Comment


def _is_anon(user: User) -> bool:
    return isinstance(user, AnonymousUser)


class Policy:
    pass


class SnippetPolicy(Policy):
    def can_create(self, user: User) -> bool:
        if _is_anon(user):
            return False
        return user.is_active

    def can_view(self, user: User, snippet: Snippet) -> bool:
        if snippet.is_public:
            return True
        return not _is_anon(user) and (user.id == snippet.author.id)

    def can_edit(self, user: User, snippet: Snippet) -> bool:
        if _is_anon(user):
            return False
        return user.id == snippet.author.id

    def can_delete(self, user: User, snippet: Snippet) -> bool:
        if _is_anon(user):
            return False
        return user.id == snippet.author.id


class CommentPolicy(Policy):
    def can_create(self, user: User, snippet: Snippet) -> bool:
        if _is_anon(user):
            return False
        if snippet.is_public:
            return True
        return user.id == snippet.author.id

    def can_view(self, user: User, comment: Comment) -> bool:
        if _is_anon(user):
            return False
        return not comment.is_deleted

    def can_edit(self, user: User, comment: Comment) -> bool:
        if _is_anon(user):
            return False
        return user.id == comment.author.id and not comment.is_deleted

    def can_delete(self, user: User, comment: Comment) -> bool:
        if _is_anon(user):
            return False
        return user.id == comment.author.id and not comment.is_deleted


class LikePolicy(Policy):
    def can_like_or_unlike(self, user: User, snippet: Snippet) -> bool:
        if _is_anon(user):
            return False
        if snippet.is_public:
            return True
        return user.id == snippet.author.id


class SharePolicy(Policy):
    def can_share(self, user: User, snippet: Snippet) -> bool:
        if _is_anon(user):
            return False

        if snippet.is_public:
            return True
        return user.id == snippet.author.id


class UserInteractionPolicy:
    def can_view_private(self, user: User, user_id: int) -> bool:
        if _is_anon(user):
            return False

        return user.id == user_id
