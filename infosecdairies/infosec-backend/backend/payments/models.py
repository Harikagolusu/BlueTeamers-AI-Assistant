from django.conf import settings
from django.db import models


class CountryPricing(models.Model):
    """Manual price overrides per country. Null fields fall back to auto-conversion from INR."""
    country_code = models.CharField(max_length=2, unique=True, help_text="ISO alpha-2 (US, GB, PK…)")
    currency_code = models.CharField(max_length=3, help_text="USD, GBP, PKR…")
    currency_symbol = models.CharField(max_length=10, help_text="$, £, ₨…")
    price_easy = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Override for easy courses (₹499 base). Leave blank for auto-convert.")
    price_medium = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Override for medium courses (₹799 base). Leave blank for auto-convert.")
    price_hard = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Override for hard courses (₹1199 base). Leave blank for auto-convert.")
    price_bundle = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Override for all-courses bundle (₹3999 base). Leave blank for auto-convert.")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Country Pricing"
        verbose_name_plural = "Country Pricing"
        ordering = ["country_code"]

    def __str__(self) -> str:
        return f"{self.country_code} ({self.currency_code})"


class PromoCode(models.Model):
    """Promo codes with usage limits and discount percentage per course."""
    code = models.CharField(max_length=50, db_index=True)
    course_slug = models.SlugField(db_index=True)
    max_uses = models.PositiveIntegerField(default=0, help_text="Maximum unique users allowed (0 = unlimited)")
    current_uses = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    discount_percent = models.PositiveIntegerField(default=100, help_text="Discount percentage (0-100). 100 = free, 50 = 50% off")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["code", "course_slug"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["code", "course_slug"], name="uniq_promo_code_per_course"),
        ]

    def __str__(self) -> str:
        return f"{self.code} ({self.current_uses}/{self.max_uses})"

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.strip().upper()
        if self.course_slug:
            self.course_slug = self.course_slug.strip()
        super().save(*args, **kwargs)

    def is_valid_for_user(self, user, *, target_course_slug: str | None = None) -> bool:
        """Check if promo code can be used by this user."""
        if not self.is_active:
            return False
        if self.max_uses > 0 and self.current_uses >= self.max_uses:
            return False

        # Global promo code (course_slug == "all"): one use per user, period.
        # Checking only against the target course would let an attacker apply
        # the same code to every course individually and enroll in all of them free.
        if self.course_slug == "all":
            if not target_course_slug:
                return False
            if PromoCodeUsage.objects.filter(code=self.code, user=user).exists():
                return False
        else:
            # Check if user already used this code for this promo row
            if PromoCodeUsage.objects.filter(promo_code=self, user=user).exists():
                return False
            # Backward compat: old usage rows stored by code/course_slug only
            if PromoCodeUsage.objects.filter(code=self.code, course_slug=self.course_slug, user=user).exists():
                return False

        return True

    def calculate_discounted_price(self, original_price: int) -> int:
        """Calculate price after applying discount."""
        if self.discount_percent >= 100:
            return 0
        if self.discount_percent <= 0:
            return original_price
        discount_amount = int(original_price * self.discount_percent / 100)
        return max(0, original_price - discount_amount)

    def record_usage(self, user, course_slug: str):
        """Record that a user used this promo code."""
        PromoCodeUsage.objects.get_or_create(
            promo_code=self,
            code=self.code,
            user=user,
            course_slug=course_slug,
        )
        self.current_uses = PromoCodeUsage.objects.filter(promo_code=self).count()
        self.save(update_fields=["current_uses"])


class PromoCodeUsage(models.Model):
    """Tracks which users have used which promo codes."""
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, related_name="usages", null=True, blank=True)
    code = models.CharField(max_length=50, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_slug = models.SlugField()
    used_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("code", "course_slug", "user")
        indexes = [
            models.Index(fields=["promo_code", "used_at"]),
            models.Index(fields=["code", "used_at"]),
            models.Index(fields=["code", "course_slug", "used_at"]),
        ]


class CoursePurchase(models.Model):
    STATUS_CREATED = "created"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Created"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_slug = models.SlugField()

    amount_inr = models.PositiveIntegerField()
    currency = models.CharField(max_length=10, default="INR")
    amount_charged = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Actual amount charged in the payment currency (e.g. 9.99 USD)"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CREATED)

    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)

    purchaser_name = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "course_slug"]),
            models.Index(fields=["razorpay_order_id"]),
        ]

    def __str__(self) -> str:  # type: ignore[override]
        return f"{self.user.email} -> {self.course_slug} ({self.status})"
