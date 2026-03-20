from django.urls import path
from .views import logout_view, resend_otp, signup_view, login_view, verify_otp
from django.contrib.auth import views as auth_views
from django_ratelimit.decorators import ratelimit

urlpatterns = [
    path("login/", login_view, name="login"),
    path("signup/", signup_view, name="signup"),
    path("verify-otp/", verify_otp, name="verify_otp"),
    path("logout/", logout_view, name="logout"),
    path("resend-otp/", resend_otp, name="resend_otp"),
]


urlpatterns += [
    path(
        "password-reset/",
        ratelimit(key="ip", rate="1/h", block=True)(
            auth_views.PasswordResetView.as_view(
                template_name="auth/password_reset.html"
            )
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
