from __future__ import annotations

from typing import Optional

from rest_framework.throttling import SimpleRateThrottle


def _client_ip(request) -> str:
    """Return the real client IP, honoring a reverse proxy.

    DRF's default ``get_ident`` uses REMOTE_ADDR, which behind Railway/Vercel
    is the shared proxy IP — throttling then becomes one global bucket (any
    user can lock out everyone, and limits don't actually bind per client).
    We take the FIRST hop of X-Forwarded-For (added by the proxy) when present.
    This is only safe when requests always arrive via a trusted proxy; when the
    app is directly reachable a client can spoof the header. Both deployments
    are handled: if NUM_PROXIES is configured we trust the header, otherwise we
    fall back to REMOTE_ADDR.
    """
    from django.conf import settings as _s

    num_proxies = getattr(_s, "NUM_PROXIES", 0) or 0
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if num_proxies > 0 and forwarded:
        # XFF lists proxy hops left-to-right: client, proxy1, proxy2. Take the
        # rightmost `num_proxies`+1 entry so a spoofed leading header is ignored.
        parts = [p.strip() for p in forwarded.split(",") if p.strip()]
        if len(parts) > num_proxies:
            return parts[-num_proxies - 1]
    return request.META.get("REMOTE_ADDR", "")


class _ProxyAwareIPThrottle(SimpleRateThrottle):
    def get_ident(self, request) -> str:
        return _client_ip(request)


class LoginIPRateThrottle(_ProxyAwareIPThrottle):
    scope = "auth_login_ip"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class RegisterIPRateThrottle(_ProxyAwareIPThrottle):
    scope = "auth_register_ip"

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated:
            return None
        ident = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}


class OTPIPRateThrottle(_ProxyAwareIPThrottle):
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
