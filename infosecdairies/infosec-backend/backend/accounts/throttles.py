from __future__ import annotations

from typing import Optional

from rest_framework.throttling import SimpleRateThrottle


class LoginIPRateThrottle(SimpleRateThrottle):
    scope = "auth_login_ip"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class RegisterIPRateThrottle(SimpleRateThrottle):
    scope = "auth_register_ip"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class OTPIPRateThrottle(SimpleRateThrottle):
    scope = "auth_otp_ip"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class EmailRateThrottle(SimpleRateThrottle):
    """Throttle requests per email address.

    This helps mitigate brute-forcing a specific user email even if IP rotates.
    """

    scope = "auth_email"

    def get_cache_key(self, request, view):
        email = None
        if isinstance(getattr(request, "data", None), dict):
            email = request.data.get("email")

        if not email:
            return None

        normalized = str(email).strip().lower()
        return self.cache_format % {"scope": self.scope, "ident": normalized}
