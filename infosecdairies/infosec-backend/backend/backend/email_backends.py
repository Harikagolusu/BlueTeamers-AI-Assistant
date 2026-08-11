import logging

import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


logger = logging.getLogger(__name__)


class ResendEmailBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        api_key = getattr(settings, "RESEND_API_KEY", "") or ""
        api_key = api_key.strip()
        if not api_key:
            raise RuntimeError("RESEND_API_KEY is not configured")

        timeout = getattr(settings, "RESEND_TIMEOUT", None)
        if timeout is None:
            timeout = getattr(settings, "EMAIL_TIMEOUT", 10)

        sent_count = 0
        for message in email_messages:
            if not message.to:
                continue

            from_email = (message.from_email or getattr(settings, "DEFAULT_FROM_EMAIL", "") or "").strip()
            if not from_email:
                raise RuntimeError("DEFAULT_FROM_EMAIL is not configured")

            payload = {
                "from": from_email,
                "to": list(message.to),
                "subject": message.subject or "",
                "text": message.body or "",
            }

            html_body = getattr(message, "alternatives", None)
            if html_body:
                for content, mimetype in html_body:
                    if mimetype == "text/html":
                        payload["html"] = content
                        break

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

            resp = requests.post(
                "https://api.resend.com/emails",
                json=payload,
                headers=headers,
                timeout=timeout,
            )

            if resp.status_code >= 400:
                logger.error(
                    "Resend email failed: status=%s body=%s to=%s subject=%s",
                    resp.status_code,
                    resp.text,
                    payload.get("to"),
                    payload.get("subject"),
                )
                if not self.fail_silently:
                    resp.raise_for_status()
                continue

            sent_count += 1

        return sent_count
