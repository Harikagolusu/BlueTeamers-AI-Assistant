"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

try:
    from django.conf import settings

    print(
        "[email-config-runtime] EMAIL_BACKEND=", getattr(settings, "EMAIL_BACKEND", None),
        "DEFAULT_FROM_EMAIL=", getattr(settings, "DEFAULT_FROM_EMAIL", None),
        "EMAIL_HOST=", getattr(settings, "EMAIL_HOST", None),
        "EMAIL_PORT=", getattr(settings, "EMAIL_PORT", None),
        "EMAIL_USE_TLS=", getattr(settings, "EMAIL_USE_TLS", None),
        "EMAIL_HOST_USER=", getattr(settings, "EMAIL_HOST_USER", None),
        flush=True,
    )
except Exception:
    pass
