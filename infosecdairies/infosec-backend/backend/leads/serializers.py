import re
from django.utils.html import strip_tags
from rest_framework import serializers
from .models import Lead

_PHONE_RE = re.compile(r'^[+\d][\d\s\-().]{5,19}$')
_NAME_RE = re.compile(r"^[\w\s'\-.,]{1,255}$", re.UNICODE)


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = ['id', 'course_name', 'name', 'email', 'phone', 'country', 'city', 'message', 'status', 'created_at', 'user']
        read_only_fields = ['id', 'status', 'created_at', 'user']

    def _no_html(self, field, value):
        if not value:
            return value
        raw = str(value).strip()
        cleaned = strip_tags(raw).strip()
        if cleaned != raw:
            raise serializers.ValidationError(f"Invalid characters in {field}.")
        return cleaned

    def validate_name(self, value):
        cleaned = self._no_html("name", value)
        if cleaned and not _NAME_RE.match(cleaned):
            raise serializers.ValidationError("Name contains invalid characters.")
        return cleaned

    def validate_course_name(self, value):
        return self._no_html("course_name", value)

    def validate_message(self, value):
        cleaned = self._no_html("message", value)
        if cleaned and len(cleaned) > 2000:
            raise serializers.ValidationError("Message too long (max 2000 characters).")
        return cleaned

    def validate_country(self, value):
        return self._no_html("country", value)

    def validate_city(self, value):
        return self._no_html("city", value)

    def validate_phone(self, value):
        cleaned = self._no_html("phone", value)
        if cleaned and not _PHONE_RE.match(cleaned):
            raise serializers.ValidationError("Enter a valid phone number (digits, +, -, spaces, parentheses only).")
        return cleaned
