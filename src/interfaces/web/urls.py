from django.urls import path
from src.interfaces.web.views.landing import handle_landing
from src.interfaces.web.views.social import (
    handle_like_snippet,
    handle_share_snippet,
    handle_share_link_created,
    handle_view_shared_snippet,
)
from src.interfaces.web.views.snippets import (
    handle_create_snippet,
    handle_snippet_detail,
    handle_edit_snippet,
    handle_my_snippets,
)
from src.interfaces.web.views.users import (
    handle_signup,
    handle_edit_profile,
    handle_author_detail,
)

from src.interfaces.web.views.search import handle_search
from django.contrib.auth import views as auth_views
from src.interfaces.web.forms.users import UserLoginForm


urlpatterns = [
    path("", handle_landing, name="landing_page"),
    path(
        "login/",
        auth_views.LoginView.as_view(authentication_form=UserLoginForm),
        name="login",
    ),
    path("signup/", handle_signup, name="signup"),
    path(
        "snippets/<int:snippet_id>/",
        handle_snippet_detail,
        name="snippet_detail",
    ),
    path(
        "snippets/<int:snippet_id>/edit/",
        handle_edit_snippet,
        name="snippet_edit",
    ),
    path(
        "snippets/new/",
        handle_create_snippet,
        name="snippet_create",
    ),
    path(
        "me/snippets/",
        handle_my_snippets,
        name="my_snippets",
    ),
    path(
        "me/edit/",
        handle_edit_profile,
        name="edit_profile",
    ),
    path(
        "snippets/<int:snippet_id>/like/",
        handle_like_snippet,
        name="like_snippet",
    ),
    path(
        "snippets/<int:snippet_id>/share/",
        handle_share_snippet,
        name="share_snippet",
    ),
    path(
        "share/<str:token>/",
        handle_view_shared_snippet,
        name="view_shared_snippet",
    ),
    path(
        "users/<int:author_id>/",
        handle_author_detail,
        name="author_detail",
    ),
    path(
        "share/<str:token>/created/",
        handle_share_link_created,
        name="share_link_created",
    ),
    path("results/", handle_search, name="search"),
]
