from django.db import models
from django.contrib.auth.models import AbstractUser
from src.domain.constants import Language


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser, BaseModel):
    about = models.TextField(blank=True)  # optional

    def __str__(self):
        return self.username


class Snippet(BaseModel):
    title = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    description = models.TextField(blank=True)  # optional
    code = models.TextField()
    language = models.CharField(
        max_length=255,
        choices=Language.choices(),
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="snippets",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class SharedSnippet(BaseModel):
    snippet = models.ForeignKey(
        Snippet,
        on_delete=models.CASCADE,
        related_name="shared_snippets",
    )
    token = models.CharField(max_length=255, unique=True, db_index=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="shared_snippets",
    )


class Comment(BaseModel):
    body = models.TextField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="comments",
    )
    snippet = models.ForeignKey(
        Snippet,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        name = self.author.username
        title = self.snippet.title
        body = self.body[:50]
        return f"{name} on '{title}': {body}"


class Like(BaseModel):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name="likes",
    )
    snippet = models.ForeignKey(
        Snippet,
        on_delete=models.CASCADE,
        related_name="likes",
    )

    class Meta:
        unique_together = ["user", "snippet"]
