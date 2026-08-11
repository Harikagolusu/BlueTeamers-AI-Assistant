from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    register,
    login,
    verify_token,
    google_jwt,
    google_onboarding,
    google_token_redirect,
    update_profile,
    google_start_otp,
    google_verify_otp,
    verify_email,
    resend_verification_otp,
    password_reset_request,
    password_reset_confirm,
)

urlpatterns = [
    path("register/", register, name="auth-register"),
    path("login/", login, name="auth-login"),
    path("verify/", verify_token, name="auth-verify-token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="auth-token-refresh"),
    path("verify-email/", verify_email, name="auth-verify-email"),
    path("resend-verification-otp/", resend_verification_otp, name="auth-resend-verification-otp"),
    path("password-reset/request/", password_reset_request, name="auth-password-reset-request"),
    path("password-reset/confirm/", password_reset_confirm, name="auth-password-reset-confirm"),
    path("google/jwt/", google_jwt, name="auth-google-jwt"),
    path("google/token-redirect/", google_token_redirect, name="auth-google-token-redirect"),
    path("google/onboarding/", google_onboarding, name="auth-google-onboarding"),
    path("google/start-otp/", google_start_otp, name="auth-google-start-otp"),
    path("google/verify-otp/", google_verify_otp, name="auth-google-verify-otp"),
    path("profile/", update_profile, name="auth-update-profile"),
]
