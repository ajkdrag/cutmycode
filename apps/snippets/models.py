import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

LANGUAGE_CHOICES = {
    "python": "Python",
    "java": "Java",
    "cpp": "C++",
}


class Snippet(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # optional
    code = models.TextField()
    language = models.CharField(max_length=255, choices=LANGUAGE_CHOICES)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="snippets"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("snippets:snippet_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return reverse("snippets:snippet_edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("snippets:snippet_delete", kwargs={"pk": self.pk})

    def get_share_url(self):
        return reverse("snippets:snippet_share", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class SharedSnippet(models.Model):
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.expires_at = timezone.now() + timedelta(days=1)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("snippets:shared_snippet_detail", kwargs={"token": self.token})

    def __str__(self):
        return f"{self.snippet.title} ({self.token})"
