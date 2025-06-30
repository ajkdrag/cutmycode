from django.urls import path
from .views import (
    DashboardView,
    SnippetDetailView,
    SnippetEditView,
    SnippetDeleteView,
    SnippetCreateView,
)

app_name = "snippets"

urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("create/", SnippetCreateView.as_view(), name="snippet_create"),
    path("<int:pk>/", SnippetDetailView.as_view(), name="snippet_detail"),
    path("<int:pk>/edit/", SnippetEditView.as_view(), name="snippet_edit"),
    path("<int:pk>/delete/", SnippetDeleteView.as_view(), name="snippet_delete"),
    # path(
    #     "<str:username>/<int: id>/<slug:slug>/",
    #     SnippetView.as_view(),
    #     name="snippet",
    # ),
]
