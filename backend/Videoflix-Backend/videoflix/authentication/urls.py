from django.urls import path
from .views import RegisterView, ConfirmEmailView, LoginView, LogoutView, password_reset, password_reset_confirm

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "confirm_email/<str:token>/", ConfirmEmailView.as_view(), name="confirm_email"
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("api/reset/password/", password_reset, name="password_reset"),
    path(
        "api/reset/password/confirm",
        password_reset_confirm,
        name="password_reset_confirm",
    ),
]
