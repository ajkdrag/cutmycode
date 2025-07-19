from django.urls import path
from .views import CustomLoginView, SignUpView, ProfileView, ProfileEditView

app_name = "accounts"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("<str:username>/", ProfileView.as_view(), name="profile_detail"),
    path("<str:username>/edit/", ProfileEditView.as_view(), name="profile_edit"),
]
