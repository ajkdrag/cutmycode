from django.db import models
from django.contrib.auth.models import AbstractUser
from src.domain.constants import Language


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractUser, BaseModel):
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
