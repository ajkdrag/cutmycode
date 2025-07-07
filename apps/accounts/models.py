from django.urls import reverse
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    def get_absolute_url(self):
        return reverse(
            "accounts:profile_detail",
            kwargs={
                "username": self.username,
            },
        )

    def get_edit_url(self):
        return reverse(
            "accounts:profile_edit",
            kwargs={
                "username": self.username,
            },
        )

    def __str__(self):
        return self.username
