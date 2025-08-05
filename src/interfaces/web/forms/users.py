from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.contrib.auth.forms import UserChangeForm
from src.data.orm.models import CustomUser


class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = CustomUser
        fields = BaseUserCreationForm.Meta.fields


class UserEditForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name"]
