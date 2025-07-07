from django.db import models
from django.conf import settings
from apps.snippets.models import Snippet
from django.urls import reverse
from django.template.defaultfilters import truncatechars


class Comment(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="comments",
    )
    snippet = models.ForeignKey(
        Snippet,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    def __str__(self):
        return truncatechars(self.body, 50)

    def get_absolute_url(self):
        return reverse("article_list")
