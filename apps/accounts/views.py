from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from .forms import CustomUserCreationForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ProfileView(TemplateView):
    template_name = "profile.html"

    class Meta:
        model = CustomUser


class ProfileEditView(UpdateView):
    model = CustomUser
    template_name = "profile_edit.html"
    slug_url_kwarg = "username"
    slug_field = "username"
    fields = ["first_name", "last_name", "username", "email"]
