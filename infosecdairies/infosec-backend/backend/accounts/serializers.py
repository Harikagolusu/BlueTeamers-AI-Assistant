from django.contrib.auth import authenticate
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from allauth.account.models import EmailAddress
from rest_framework import serializers

from .models import User, AuthProvider


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=10)

    class Meta:
        model = User
        fields = ["full_name", "email", "password", "mobile"]

    def validate_full_name(self, value):
        # Prevent stored XSS: do not allow HTML/JS in names.
        raw = (value or "").strip()
        cleaned = strip_tags(raw).strip()
        if cleaned != raw:
            raise serializers.ValidationError("Invalid characters in name.")
        if len(cleaned) < 2:
            raise serializers.ValidationError("Name is too short.")
        if len(cleaned) > 255:
            raise serializers.ValidationError("Name is too long.")
        return cleaned

    def validate_password(self, value):
        password = value or ""
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return password

    def validate_mobile(self, value):
        if value in (None, ""):
            return value
        raw = str(value).strip()
        cleaned = strip_tags(raw).strip()
        if cleaned != raw:
            raise serializers.ValidationError("Invalid characters in mobile.")
        if len(cleaned) > 20:
            raise serializers.ValidationError("Mobile is too long.")
        return cleaned

    def validate_email(self, value):
        """Check if user with this email already exists."""
        email = value.lower().strip()
        if "@" not in email:
            raise serializers.ValidationError("Invalid email address.")

        allowed_domains = getattr(settings, "ALLOWED_EMAIL_DOMAINS", None)
        if allowed_domains:
            domain = email.split("@", 1)[1]
            allowed = {str(d).strip().lower() for d in allowed_domains if str(d).strip()}
            if allowed and domain not in allowed:
                raise serializers.ValidationError("Email domain is not allowed.")

        block_disposable = getattr(settings, "BLOCK_DISPOSABLE_EMAILS", True)
        if block_disposable and "@" in email:
            domain = email.split("@", 1)[1]
            blocked_domains = set(
                d.strip().lower()
                for d in getattr(
                    settings,
                    "DISPOSABLE_EMAIL_DOMAINS",
                    [
                        "mailinator.com",
                        "guerrillamail.com",
                        "guerrillamail.info",
                        "guerrillamail.net",
                        "sharklasers.com",
                        "yopmail.com",
                        "yopmail.fr",
                        "yopmail.net",
                        "temp-mail.org",
                        "10minutemail.com",
                        "10minutemail.net",
                        "mohmal.com",
                        "dispostable.com",
                        "getnada.com",
                    ],
                )
                if d.strip()
            )
            if domain in blocked_domains:
                raise serializers.ValidationError("Disposable email addresses are not allowed.")
        existing = User.objects.filter(email=email).first()
        if existing:
            # Block re-registration only for active/verified accounts, or social accounts.
            # An inactive+unverified email account means the user registered but never
            # completed OTP verification (e.g. closed the tab). We allow re-registration
            # so they can get a fresh OTP instead of being permanently stuck.
            if existing.is_active or existing.is_verified or existing.auth_provider != AuthProvider.EMAIL:
                raise serializers.ValidationError(
                    "An account with this email already exists. Please sign in instead."
                )
        return email

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("is_active", None)
        validated_data.pop("is_verified", None)
        validated_data.pop("is_staff", None)
        validated_data.pop("is_superuser", None)

        email = validated_data.get("email")

        # Re-registration: update the stale unverified account instead of creating a duplicate
        existing = User.objects.filter(
            email=email, is_active=False, is_verified=False, auth_provider=AuthProvider.EMAIL
        ).first()
        if existing:
            existing.full_name = validated_data.get("full_name", existing.full_name)
            existing.mobile = validated_data.get("mobile", existing.mobile)
            existing.set_password(password)
            existing.save(update_fields=["full_name", "mobile", "password"])
            return existing

        user = User(
            full_name=validated_data.get("full_name"),
            email=email,
            mobile=validated_data.get("mobile"),
            auth_provider=AuthProvider.EMAIL,
            is_active=False,
            is_verified=False,
        )
        user.set_password(password)
        user.save()

        EmailAddress.objects.get_or_create(
            user=user,
            email=user.email,
            defaults={"verified": False, "primary": True},
        )

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        try:
            existing_user = User.objects.get(email=str(email).strip().lower())
        except User.DoesNotExist:
            existing_user = None

        if existing_user and existing_user.auth_provider == AuthProvider.GOOGLE and not existing_user.has_usable_password():
            raise serializers.ValidationError("This account was created with Google. Please continue with Google.")

        user = authenticate(request=self.context.get("request"), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")

        # Uniform message even for unverified/inactive accounts: returning a
        # distinct "please verify" string here lets an attacker enumerate which
        # emails have registered accounts. Unverified users use the dedicated
        # resend-verification-otp endpoint to complete signup.
        if not user.is_active:
            raise serializers.ValidationError("Invalid email or password")

        attrs["user"] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "mobile", "auth_provider"]
