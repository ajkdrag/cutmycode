from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

from src.data.orm.models import CustomUser


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "c-input"})
        self.fields["password"].widget.attrs.update({"class": "c-input"})


class UserCreationForm(DjangoUserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "c-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "c-input"})
        self.fields["password2"].widget.attrs.update({"class": "c-input"})


class UserEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "about"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "c-input"}),
            "first_name": forms.TextInput(attrs={"class": "c-input"}),
            "last_name": forms.TextInput(attrs={"class": "c-input"}),
            "about": forms.Textarea(attrs={"class": "c-textarea"}),
        }
