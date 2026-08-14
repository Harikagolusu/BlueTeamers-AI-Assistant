import os
import secrets

from django.core.management.base import BaseCommand
from payments.models import PromoCode


class Command(BaseCommand):
    help = "Seed promo codes with usage limits (codes configurable via env)"

    def handle(self, *args, **options):
        # Codes are configurable via the PROMO_CODES_JSON env var:
        #   [{"code": "...", "course_slug": "...", "max_uses": 10,
        #     "is_active": true, "discount_percent": 100}, ...]
        # Defaults are RANDOM unguessable codes (not dictionary words) so a
        # reader of the source cannot redeem 100%-off courses. Previously this
        # file shipped guessable codes like HEHE100 / BLUETEAMFREE / SIEMFREE.
        import json as _json

        raw = os.getenv("PROMO_CODES_JSON", "")
        if raw:
            try:
                promo_codes = [
                    (
                        item["code"],
                        item["course_slug"],
                        int(item.get("max_uses", 10)),
                        bool(item.get("is_active", True)),
                        int(item.get("discount_percent", 100)),
                    )
                    for item in _json.loads(raw)
                ]
            except Exception as exc:
                self.stderr.write(f"Invalid PROMO_CODES_JSON: {exc}")
                promo_codes = _default_codes()
        else:
            promo_codes = _default_codes()

        created_count = 0
        updated_count = 0

        for code, course_slug, max_uses, is_active, discount_percent in promo_codes:
            obj, created = PromoCode.objects.update_or_create(
                code=code,
                course_slug=course_slug,
                defaults={
                    "max_uses": max_uses,
                    "is_active": is_active,
                    "discount_percent": discount_percent,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {code} -> {course_slug} (max: {max_uses}, {discount_percent}% off)"))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f"Updated: {code} -> {course_slug} (max: {max_uses}, {discount_percent}% off)"))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created {created_count}, Updated {updated_count} promo codes."
        ))


def _default_codes() -> list:
    """Random unguessable 100%-off codes per course.

    Generate your own for a real campaign and pass via PROMO_CODES_JSON. The
    codes below are regenerated on every seed run from a strong RNG.
    """
    def _rand() -> str:
        return "BT-" + secrets.token_hex(6).upper()

    return [
        (_rand(), "blue-team-soc-fundamentals", 10, True, 100),
        (_rand(), "blue-team-soc-fundamentals", 10, True, 100),
        (_rand(), "blue-team-soc-fundamentals", 10, True, 100),
        (_rand(), "blue-team-soc-fundamentals", 15, True, 100),
        (_rand(), "blue-team-soc-fundamentals", 17, True, 100),
        (_rand(), "blue-team-soc-fundamentals", 7, True, 100),
        (_rand(), "log-analysis", 7, True, 100),
        (_rand(), "siem-fundamentals", 7, True, 100),
        (_rand(), "network-security-monitoring", 7, True, 100),
        (_rand(), "incident-response", 7, True, 100),
        (_rand(), "threat-hunting", 7, True, 100),
        (_rand(), "detection-engineering", 7, True, 100),
        (_rand(), "malware-analysis", 7, True, 100),
        (_rand(), "soc-analyst-path", 7, True, 100),
    ]
