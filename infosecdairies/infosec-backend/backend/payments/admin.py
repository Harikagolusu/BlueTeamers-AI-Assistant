from django import forms
from django.contrib import admin

from courses.models import Course
from .models import CoursePurchase, PromoCode, PromoCodeUsage, CountryPricing


DISCOUNT_CHOICES = [
    (10,  "10% off"),
    (15,  "15% off"),
    (20,  "20% off"),
    (25,  "25% off"),
    (30,  "30% off"),
    (40,  "40% off"),
    (50,  "50% off"),
    (60,  "60% off"),
    (75,  "75% off"),
    (90,  "90% off"),
    (100, "100% — Free access"),
]

# Static slug choices that aren't individual courses
STATIC_SLUG_CHOICES = [
    ("all",                "All Courses (applies to any course / bundle)"),
    ("all-courses-bundle", "All Courses Bundle (bundle checkout only)"),
]


def _course_slug_choices():
    """Build choices from published courses in the DB, with friendly names."""
    choices = list(STATIC_SLUG_CHOICES)
    try:
        for c in Course.objects.filter(is_published=True).order_by("title"):
            label = f"{c.title}  [{c.slug}]"
            choices.append((c.slug, label))
    except Exception:
        pass
    return choices


class PromoCodeForm(forms.ModelForm):
    course_slug = forms.ChoiceField(
        choices=[],  # populated in __init__ so it queries DB fresh each time
        help_text="Choose which course this promo applies to. 'All Courses' works on every course and the bundle.",
    )
    discount_percent = forms.ChoiceField(
        choices=DISCOUNT_CHOICES,
        help_text="Discount percentage. 100 = fully free, 50 = half price, etc.",
    )

    class Meta:
        model = PromoCode
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course_slug"].choices = _course_slug_choices()
        # Pre-select current value when editing an existing record
        if self.instance and self.instance.pk:
            self.fields["course_slug"].initial = self.instance.course_slug
            self.fields["discount_percent"].initial = self.instance.discount_percent

    def clean_discount_percent(self):
        return int(self.cleaned_data["discount_percent"])


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    form = PromoCodeForm
    list_display = ("id", "code", "course_slug", "discount_percent", "is_active", "current_uses", "max_uses", "created_at")
    search_fields = ("code", "course_slug")
    list_filter = ("is_active", "course_slug")


@admin.register(CoursePurchase)
class CoursePurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course_slug",
        "amount_inr",
        "amount_charged",
        "currency",
        "status",
        "razorpay_order_id",
        "razorpay_payment_id",
        "created_at",
        "paid_at",
    )
    search_fields = ("course_slug", "razorpay_order_id", "razorpay_payment_id", "user__email")
    list_filter = ("status", "course_slug", "currency")


@admin.register(CountryPricing)
class CountryPricingAdmin(admin.ModelAdmin):
    list_display = ("country_code", "currency_code", "currency_symbol", "price_easy", "price_medium", "price_hard", "price_bundle", "is_active")
    list_editable = ("price_easy", "price_medium", "price_hard", "price_bundle", "is_active")
    list_filter = ("is_active",)
    search_fields = ("country_code", "currency_code")
    ordering = ("country_code",)


@admin.register(PromoCodeUsage)
class PromoCodeUsageAdmin(admin.ModelAdmin):
    list_display = ("id", "promo_code", "code", "user", "course_slug", "used_at")
    search_fields = ("code", "promo_code__code", "promo_code__course_slug", "user__email")
    list_filter = ("course_slug", "used_at")
