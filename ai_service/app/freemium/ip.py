"""Server-side guest-IP derivation for freemium enforcement.

The anonymous daily allowance is anchored to the caller's source IP as well as
the client-supplied ``client_id`` so that rotating the id (or clearing the
browser's localStorage key) can no longer mint a fresh quota.

The service is normally reached through a reverse proxy (CloudFront in
production, the Vite dev proxy locally), so the direct transport peer is the
proxy's address. The real viewer IP is recovered from the *right-most*
``X-Forwarded-For`` entry when the direct peer is a trusted (private/loopback)
hop: the innermost trusted proxy appends the true client address, while earlier
entries are client-controllable and therefore ignored. A public direct peer is
trusted as itself and never let the client report its own IP.
"""
from typing import Optional

from starlette.requests import Request


def extract_client_ip(request: Request) -> Optional[str]:
    """Return the caller's source IP for freemium keying, or None when unknown.

    When FREEMIUM_TRUST_XFF is False (default), the direct transport peer is
    authoritative and X-Forwarded-For is ignored, preventing spoofing when the
    service is directly exposed without a trusted proxy.
    """
    from app.core.config import settings

    if not request.client or not request.client.host:
        return None
    peer = request.client.host
    # Only trust XFF when explicitly enabled
    if not getattr(settings, "FREEMIUM_TRUST_XFF", False):
        return peer
    xff = request.headers.get("x-forwarded-for")
    parts = [p.strip().strip("\"'").strip() for p in xff.split(",") if p.strip()] if isinstance(xff, str) else []
    if parts and _is_trusted_proxy(peer):
        return parts[-1]
    return peer


def _is_trusted_proxy(peer: str) -> bool:
    """Whether the direct transport peer may be an intermediary we trust.

    Private / loopback ranges are treated as trusted proxies: when the direct
    hop is 127.0.0.1 (Vite) or a private LB/edge, the real viewer IP must come
    from the forwarding headers. Any other peer is assumed to be the client.
    """
    if peer.startswith("::ffff:"):
        # IPv4-mapped IPv6 form (e.g. "::ffff:127.0.0.1") seen on :: listeners
        return _is_trusted_proxy(peer[len("::ffff:"):])
    if peer.startswith("::"):
        return peer in ("::1", "0:0:0:0:0:0:0:1")
    if peer.startswith(("127.", "10.", "192.168.", "0.")):
        return True
    if peer.startswith("172."):
        try:
            second = int(peer.split(".")[1])
        except (IndexError, ValueError):
            return False
        return 16 <= second <= 31
    return False