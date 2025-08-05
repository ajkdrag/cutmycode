from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from src.interfaces.web.forms.users import (
    UserCreationForm,
    UserEditForm,
)


def handle_signup(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "registration/signup.html", {"form": form})


@login_required(login_url="login")
def handle_edit_profile(request):
    form = UserEditForm(
        request.POST or None,
        instance=request.user,
    )
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("my_snippets")
    return render(request, "users/edit_profile.html", {"form": form})
