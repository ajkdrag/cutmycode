from django.db import models
from django.conf import settings
from django.urls import reverse


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

    def __str__(self):
        return self.title
