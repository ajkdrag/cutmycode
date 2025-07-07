from django.urls import path
from .views import CommentCreateView

app_name = "comments"

urlpatterns = [
    path("<int:pk>/create/", CommentCreateView.as_view(), name="post-comment")
]
