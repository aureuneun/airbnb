from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github/", views.github_login, name="github-login"),
    path("login/github/callback/", views.github_callback, name="github-callback"),
    path("login/kakao/", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback/", views.kakao_callback, name="kakao-callback"),
    path("logout/", views.log_out, name="logout"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "verify/<str:code>/", views.complete_verification, name="complete-verification"
    ),
    path("edit-profile/", views.EditProfileView.as_view(), name="edit-profile"),
    path(
        "change-password/", views.ChangePasswordView.as_view(), name="change-password"
    ),
    path("<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("toggle-hosting/", views.toggle_hosting, name="toggle-hosting"),
    path("switch-language/", views.switch_language, name="switch-language"),
]