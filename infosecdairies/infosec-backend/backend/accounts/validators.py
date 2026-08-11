from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class PasswordComplexityValidator:
    def validate(self, password, user=None):
        if password is None:
            raise ValidationError(_("Password is required."), code="password_required")

        if not re.search(r"[a-z]", password):
            raise ValidationError(_("Password must contain a lowercase letter."), code="password_no_lower")
        if not re.search(r"[A-Z]", password):
            raise ValidationError(_("Password must contain an uppercase letter."), code="password_no_upper")
        if not re.search(r"\d", password):
            raise ValidationError(_("Password must contain a number."), code="password_no_digit")
        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError(_("Password must contain a symbol."), code="password_no_symbol")

    def get_help_text(self):
        return _("Your password must contain at least one lowercase letter, one uppercase letter, one number, and one symbol.")


class MaximumLengthValidator:
    """Reject passwords longer than max_length characters.

    Plugs into AUTH_PASSWORD_VALIDATORS so it applies everywhere
    validate_password() is called: registration, password reset, Google onboarding.
    """

    def __init__(self, max_length=15):
        self.max_length = max_length

    def validate(self, password, user=None):
        if password and len(password) > self.max_length:
            raise ValidationError(
                _(f"Password must be at most {self.max_length} characters."),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self):
        return _(f"Your password must contain no more than {self.max_length} characters.")
