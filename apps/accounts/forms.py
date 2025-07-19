from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "c-input",
                "placeholder": "Username or email",
                "autocomplete": "username",
                "autofocus": True,
            }
        ),
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "c-input",
                "autocomplete": "current-password",
                "aria-describedby": "password-help",
            }
        ),
    )
