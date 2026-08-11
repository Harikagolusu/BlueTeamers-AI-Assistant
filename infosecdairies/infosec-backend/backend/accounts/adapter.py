"""Custom allauth adapter to link social accounts to existing users by email."""

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

_ALLOWED_FRONTEND_HOSTS = {
    "infosecdairies.io",
    "www.infosecdairies.io",
    "blueteamers.io",
    "www.blueteamers.io",
}


class CustomAccountAdapter(DefaultAccountAdapter):
    """Allow post-OAuth redirects to either production frontend domain."""

    def is_safe_url(self, url):
        from django.utils.http import url_has_allowed_host_and_scheme

        allowed = set(_ALLOWED_FRONTEND_HOSTS)
        if settings.DEBUG:
            allowed.update({"localhost", "localhost:8081", "127.0.0.1", "127.0.0.1:8081"})
        return url_has_allowed_host_and_scheme(url, allowed_hosts=allowed, require_https=not settings.DEBUG)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter that connects social logins to existing users with the same email.
    
    This prevents creating duplicate user accounts when a user who previously
    signed up with email/password later signs in with Google (or vice versa).
    """

    def pre_social_login(self, request, sociallogin):
        """
        Called before the social login is processed.
        
        If a user with the same email already exists, connect the social account
        to that existing user instead of creating a new one.
        Also ensures user is marked as verified when using social auth.
        """
        # Skip if user is already connected
        if sociallogin.user.pk:
            # User already exists. Only mark them verified if they're not an
            # unverified email-registered account — those must still complete
            # OTP verification before we grant full JWT access. Blindly setting
            # is_verified=True here would let anyone bypass email OTP by using
            # Google OAuth with the same email address.
            user = sociallogin.user
            from accounts.models import AuthProvider
            email_unverified = (
                getattr(user, "auth_provider", None) == AuthProvider.EMAIL
                and not user.is_verified
            )
            if not email_unverified:
                updated = False
                if getattr(sociallogin.account, "provider", None) == "google":
                    if getattr(user, "auth_provider", None) != "google":
                        user.auth_provider = "google"
                        updated = True
                if not user.is_verified:
                    user.is_verified = True
                    updated = True
                if not user.is_active:
                    user.is_active = True
                    updated = True
                if updated:
                    user.save()
            return

        email = sociallogin.user.email
        if not email:
            return

        # Normalize email for lookup
        email = email.lower().strip()

        try:
            # Check if a user with this email already exists
            existing_user = User.objects.get(email=email)
            
            # Check if this social account is already connected
            social_account_exists = SocialAccount.objects.filter(
                user=existing_user,
                provider=sociallogin.account.provider,
                uid=sociallogin.account.uid
            ).exists()
            
            if not social_account_exists:
                # Connect the social login to the existing user
                sociallogin.user = existing_user
                sociallogin.account.user = existing_user
                
            # Only auto-verify via social auth if the user is already verified,
            # or if their account was originally created via a social provider.
            # Never bypass email OTP for unverified email-registered accounts —
            # doing so would let anyone use Google OAuth to activate an account
            # they don't own (the OTP was sent to the real owner's inbox).
            from accounts.models import AuthProvider
            email_unverified = (
                getattr(existing_user, "auth_provider", None) == AuthProvider.EMAIL
                and not existing_user.is_verified
            )
            updated = False
            if not email_unverified:
                if not existing_user.is_verified:
                    existing_user.is_verified = True
                    updated = True
                if not existing_user.is_active:
                    existing_user.is_active = True
                    updated = True
            if getattr(sociallogin.account, "provider", None) == "google" and getattr(existing_user, "auth_provider", None) != "google" and not email_unverified:
                existing_user.auth_provider = "google"
                updated = True
            if updated:
                existing_user.save()
                
        except User.DoesNotExist:
            # No existing user with this email — new account creation.
            # Brand new Google user: require onboarding + OTP before issuing JWT.
            if getattr(sociallogin.account, "provider", None) == "google":
                user = sociallogin.user
                try:
                    if getattr(user, "auth_provider", None) != "google":
                        user.auth_provider = "google"
                    user.set_unusable_password()
                    user.is_verified = False
                    user.save()
                except Exception:
                    pass

    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Allow auto-signup. The adapter's pre_social_login handles user linking.
        """
        return True

    def get_connect_redirect_url(self, request, socialaccount):
        """
        Return the URL to redirect to after connecting a social account.
        """
        return '/'
