import hashlib
import hmac
from datetime import datetime
import logging

import requests as _http
import razorpay
from razorpay.errors import BadRequestError
from django.conf import settings
from django.core.cache import cache as _django_cache
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from courses.models import Course, Enrollment
from accounts.email_templates import _send_html_email, get_payment_receipt_template

from .models import CoursePurchase, PromoCode, PromoCodeUsage, CountryPricing
from .exchange_rates import inr_to_currency, COUNTRY_CURRENCY_MAP


logger = logging.getLogger(__name__)


def _payment_rate_limit(key: str, limit: int, period: int) -> bool:
    """Return True if the caller exceeded the rate limit."""
    count = _django_cache.get(key, 0)
    if count >= limit:
        return True
    _django_cache.set(key, count + 1, period)
    return False


def _get_client_ip(request) -> str:
    """Return the real client IP, handling Railway's reverse-proxy X-Forwarded-For."""
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _get_country_from_ip(ip: str) -> str:
    """Resolve a 2-letter ISO country code from an IP address. Cached 24 hrs. Falls back to IN."""
    if not ip or ip in ("127.0.0.1", "::1"):
        return "IN"
    cache_key = f"ip_country:{ip}"
    cached = _django_cache.get(cache_key)
    if cached:
        return cached
    try:
        resp = _http.get(f"https://ipapi.co/{ip}/country/", timeout=3, headers={"User-Agent": "infosecdairies/1.0"})
        if resp.ok and len(resp.text.strip()) == 2:
            country = resp.text.strip().upper()
            _django_cache.set(cache_key, country, 86400)
            return country
    except Exception:
        logger.warning("IP country lookup failed for %s", ip)
    return "IN"


FREE_COURSE_SLUG = "network-fundamentals"
ALL_COURSES_BUNDLE_SLUG = "all-courses-bundle"
ALL_COURSES_BUNDLE_PRICE_INR = 3999

# URL slugs (sent by frontend) → canonical promo code course slugs (stored in DB)
_URL_SLUG_TO_PROMO_SLUG = {
    "malware-analysis-fundamentals": "malware-analysis",
    "log-analysis-for-beginners": "log-analysis",
    "incident-response-fundamentals": "incident-response",
    "threat-hunting-fundamentals": "threat-hunting",
    "detection-engineering-basics": "detection-engineering",
    "soc-analyst-practical-training": "soc-analyst-practical",
}


def _promo_course_slug(course_slug: str) -> str:
    return _URL_SLUG_TO_PROMO_SLUG.get(course_slug, course_slug)


def _difficulty_price_inr(level: str) -> int:
    lvl = (level or "").strip().lower()
    if lvl in ["beginner", "easy"]:
        return 499
    if lvl in ["intermediate", "medium"]:
        return 799
    if lvl in ["advanced", "hard"]:
        return 1199
    return 499


def _is_test_mode() -> bool:
    if not getattr(settings, "PAYMENTS_TEST_MODE", False):
        return False
    # Block test mode in production to prevent payment bypass
    is_prod = bool(getattr(settings, "RAILWAY_PUBLIC_DOMAIN", "") or getattr(settings, "RAILWAY_ENVIRONMENT", ""))
    if is_prod:
        logger.error("PAYMENTS_TEST_MODE=True is blocked in production — ignoring")
        return False
    return True


def _course_price_inr(course: Course) -> int:
    if course.slug == FREE_COURSE_SLUG:
        return 0
    if _is_test_mode():
        return _difficulty_price_inr(course.level)
    return _difficulty_price_inr(course.level)


def _bundle_price_inr() -> int:
    if _is_test_mode():
        return ALL_COURSES_BUNDLE_PRICE_INR
    return ALL_COURSES_BUNDLE_PRICE_INR


def _get_local_price(country_code: str, tier: str, inr_amount: int) -> dict:
    """
    Returns {amount, currency, symbol} for a given country and INR base price.
    Checks CountryPricing for manual override first; falls back to live rate conversion.
    tier must be one of: easy, medium, hard, bundle
    """
    code = (country_code or "").upper().strip()

    try:
        pricing = CountryPricing.objects.filter(country_code=code, is_active=True).first()
    except Exception:
        return {"amount": float(inr_amount), "currency": "INR", "symbol": "₹"}

    if pricing:
        manual = getattr(pricing, f"price_{tier}", None)
        if manual is not None:
            return {"amount": float(manual), "currency": pricing.currency_code, "symbol": pricing.currency_symbol}
        currency_code = pricing.currency_code
        symbol = pricing.currency_symbol
    elif code in COUNTRY_CURRENCY_MAP:
        currency_code, symbol = COUNTRY_CURRENCY_MAP[code]
    else:
        return {"amount": float(inr_amount), "currency": "INR", "symbol": "₹"}

    converted = inr_to_currency(inr_amount, currency_code)
    return {"amount": converted, "currency": currency_code, "symbol": symbol}


def _clean_razorpay_cred(value: str) -> str:
    """Best-effort sanitization for env-provided secrets."""
    v = (value or "").strip()
    if (v.startswith("(") and v.endswith(")")):
        v = v[1:-1].strip()
    return v


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    # Rate limit: 10 order creations per user per minute
    if _payment_rate_limit(f"pay_create:{request.user.id}", 10, 60):
        return Response({"detail": "Too many requests. Please wait a moment."}, status=429)

    course_slug = request.data.get("course_slug")
    purchaser_name = request.data.get("full_name")
    promo_code = request.data.get("promo_code", "").strip().upper()
    country_code = _get_country_from_ip(_get_client_ip(request))

    if not course_slug:
        return Response({"detail": "course_slug is required"}, status=400)

    promo_slug = _promo_course_slug(course_slug)

    is_promo_valid = False
    promo_code_obj = None
    if promo_code:
        promo_code_obj = (
            PromoCode.objects.filter(code=promo_code, is_active=True, course_slug=promo_slug).first()
            or PromoCode.objects.filter(code=promo_code, is_active=True, course_slug="all").first()
        )
        if not promo_code_obj:
            return Response({"detail": "Invalid promo code"}, status=400)

        if promo_code_obj.is_valid_for_user(request.user, target_course_slug=promo_slug):
            is_promo_valid = True
        else:
            if promo_code_obj.current_uses >= promo_code_obj.max_uses and promo_code_obj.max_uses > 0:
                return Response({"detail": "This promo code has reached its usage limit"}, status=400)
            if PromoCodeUsage.objects.filter(code=promo_code, user=request.user, course_slug=promo_slug).exists():
                _is_bundle = course_slug == ALL_COURSES_BUNDLE_SLUG
                _c = None if _is_bundle else Course.objects.filter(slug=course_slug, is_published=True).first()
                _enrolled = _is_bundle or (
                    _c is not None and Enrollment.objects.filter(user=request.user, course=_c, is_paid=True).exists()
                )
                if _enrolled:
                    return Response({"free": True, "course_slug": course_slug, "amount_inr": 0})
                retry_key = f"promo_retry:{request.user.id}:{promo_code}:{promo_slug}"
                retry_count = _django_cache.get(retry_key, 0)
                if retry_count >= 3:
                    return Response(
                        {"detail": "Too many promo code retry attempts. Please contact support."},
                        status=429,
                    )
                _django_cache.set(retry_key, retry_count + 1, 3600)
                is_promo_valid = True
                promo_code_obj._skip_record_usage = True
            else:
                return Response({"detail": "Invalid or inactive promo code"}, status=400)

    is_bundle = course_slug == ALL_COURSES_BUNDLE_SLUG
    course = None
    if not is_bundle:
        course = get_object_or_404(Course, slug=course_slug, is_published=True)
        amount_inr = _course_price_inr(course)
        lvl = (course.level or "easy").strip().lower()
        if lvl in ("beginner",):
            tier = "easy"
        elif lvl in ("intermediate",):
            tier = "medium"
        elif lvl in ("advanced",):
            tier = "hard"
        elif lvl in ("easy", "medium", "hard"):
            tier = lvl
        else:
            tier = "easy"
    else:
        amount_inr = _bundle_price_inr()
        tier = "bundle"

    if is_promo_valid and promo_code_obj:
        amount_inr = promo_code_obj.calculate_discounted_price(amount_inr)
        if not getattr(promo_code_obj, "_skip_record_usage", False):
            with transaction.atomic():
                locked = PromoCode.objects.select_for_update().get(pk=promo_code_obj.pk)
                if locked.max_uses > 0 and locked.current_uses >= locked.max_uses:
                    return Response({"detail": "This promo code has reached its usage limit"}, status=400)
                locked.record_usage(request.user, promo_slug)

    if amount_inr == 0:
        if not is_bundle:
            course = get_object_or_404(Course, slug=course_slug, is_published=True)
            enrollment, _ = Enrollment.objects.get_or_create(
                user=request.user, course=course, defaults={"is_paid": True},
            )
            if not enrollment.is_paid:
                enrollment.is_paid = True
                enrollment.save(update_fields=["is_paid"])
        else:
            courses = Course.objects.filter(is_published=True)
            for c in courses:
                enrollment, _ = Enrollment.objects.get_or_create(
                    user=request.user, course=c, defaults={"is_paid": True},
                )
                if not enrollment.is_paid:
                    enrollment.is_paid = True
                    enrollment.save(update_fields=["is_paid"])
        # Record a zero-amount purchase so my-purchases reflects free promo access
        import uuid as _uuid
        CoursePurchase.objects.get_or_create(
            user=request.user,
            course_slug=course_slug,
            status=CoursePurchase.STATUS_PAID,
            defaults={
                "amount_inr": 0,
                "amount_charged": 0,
                "currency": "INR",
                "razorpay_order_id": f"free_{_uuid.uuid4().hex[:20]}",
                "purchaser_name": purchaser_name or "",
                "paid_at": timezone.now(),
            },
        )
        return Response({
            "free": True, "course_slug": course_slug, "amount_inr": 0,
            "discount_percent": promo_code_obj.discount_percent if promo_code_obj else None,
        })

    existing_paid = CoursePurchase.objects.filter(
        user=request.user, course_slug=course_slug, status=CoursePurchase.STATUS_PAID,
    ).exists()
    if existing_paid:
        return Response({"already_paid": True, "course_slug": course_slug, "amount_inr": amount_inr})

    # Resolve local currency amount
    local = _get_local_price(country_code, tier, amount_inr)
    local_amount = local["amount"]
    local_currency = local["currency"]
    local_symbol = local["symbol"]

    # Razorpay requires amount in smallest denomination (×100 for all supported currencies)
    razorpay_amount = int(round(local_amount * 100))

    key_id = _clean_razorpay_cred(getattr(settings, "RAZORPAY_KEY_ID", ""))
    key_secret = _clean_razorpay_cred(getattr(settings, "RAZORPAY_KEY_SECRET", ""))

    if _is_test_mode() and (not key_id or not key_secret):
        import uuid
        mock_order_id = f"mock_order_{uuid.uuid4().hex[:16]}"
        CoursePurchase.objects.create(
            user=request.user,
            course_slug=course_slug,
            amount_inr=amount_inr,
            amount_charged=local_amount,
            currency=local_currency,
            status=CoursePurchase.STATUS_CREATED,
            razorpay_order_id=mock_order_id,
            purchaser_name=purchaser_name,
        )
        return Response({
            "free": False,
            "key_id": "test_key_placeholder",
            "order_id": mock_order_id,
            "amount": razorpay_amount,
            "currency": local_currency,
            "amount_display": local_amount,
            "symbol": local_symbol,
            "course_slug": course_slug,
            "amount_inr": amount_inr,
            "test_mode": True,
        })

    if not key_id or not key_secret:
        return Response({"detail": "Razorpay is not configured"}, status=500)
    if not key_id.startswith("rzp_"):
        return Response({"detail": "Invalid Razorpay Key ID"}, status=500)

    client = razorpay.Client(auth=(key_id, key_secret))
    receipt = f"course_{course_slug}_{request.user.id}_{int(datetime.utcnow().timestamp())}"
    receipt = receipt[:40]

    try:
        order = client.order.create({
            "amount": razorpay_amount,
            "currency": local_currency,
            "receipt": receipt,
            "payment_capture": 1,
            "notes": {
                "course_slug": course_slug,
                "user_id": str(request.user.id),
            },
        })
    except BadRequestError as exc:
        return Response({"detail": str(exc)}, status=502)

    CoursePurchase.objects.create(
        user=request.user,
        course_slug=course_slug,
        amount_inr=amount_inr,
        amount_charged=local_amount,
        currency=local_currency,
        status=CoursePurchase.STATUS_CREATED,
        razorpay_order_id=order["id"],
        purchaser_name=purchaser_name,
    )

    return Response({
        "free": False,
        "key_id": key_id,
        "order_id": order["id"],
        "amount": razorpay_amount,
        "currency": local_currency,
        "amount_display": local_amount,
        "symbol": local_symbol,
        "course_slug": course_slug,
        "amount_inr": amount_inr,
        "discount_percent": promo_code_obj.discount_percent if promo_code_obj else None,
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    # Rate limit: 10 verification attempts per user per minute
    if _payment_rate_limit(f"pay_verify:{request.user.id}", 10, 60):
        return Response({"detail": "Too many payment verification attempts. Please wait."}, status=429)

    order_id = request.data.get("razorpay_order_id")
    payment_id = request.data.get("razorpay_payment_id")
    signature = request.data.get("razorpay_signature")

    if not order_id or not payment_id or not signature:
        return Response({"detail": "Missing payment fields"}, status=400)

    purchase = get_object_or_404(CoursePurchase, user=request.user, razorpay_order_id=order_id)

    if purchase.status == CoursePurchase.STATUS_PAID:
        return Response({"success": True, "course_slug": purchase.course_slug, "already_paid": True})

    key_secret = _clean_razorpay_cred(getattr(settings, "RAZORPAY_KEY_SECRET", ""))
    
    # Test mode: skip signature verification
    is_test_mode = _is_test_mode()
    is_test_order = order_id.startswith("mock_order_")
    
    if is_test_mode and is_test_order:
        # In test mode, auto-approve test orders
        purchase.status = CoursePurchase.STATUS_PAID
        purchase.razorpay_payment_id = payment_id or "generic_payment_id"
        purchase.razorpay_signature = signature or "generic_signature"
        purchase.paid_at = timezone.now()
        purchase.save(update_fields=["status", "razorpay_payment_id", "razorpay_signature", "paid_at"])
    elif not key_secret:
        return Response({"detail": "Razorpay is not configured"}, status=500)
    else:
        msg = f"{order_id}|{payment_id}".encode("utf-8")
        expected = hmac.new(key_secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(expected, signature):
            purchase.status = CoursePurchase.STATUS_FAILED
            purchase.razorpay_payment_id = payment_id
            purchase.razorpay_signature = signature
            purchase.save(update_fields=["status", "razorpay_payment_id", "razorpay_signature"])
            return Response({"detail": "Invalid payment signature"}, status=400)

        purchase.status = CoursePurchase.STATUS_PAID
        purchase.razorpay_payment_id = payment_id
        purchase.razorpay_signature = signature
        purchase.paid_at = timezone.now()
        purchase.save(update_fields=["status", "razorpay_payment_id", "razorpay_signature", "paid_at"])

    if purchase.course_slug == ALL_COURSES_BUNDLE_SLUG:
        courses = Course.objects.filter(is_published=True)
        for c in courses:
            enrollment, _ = Enrollment.objects.get_or_create(
                user=request.user,
                course=c,
                defaults={"is_paid": True},
            )
            if not enrollment.is_paid:
                enrollment.is_paid = True
                enrollment.save(update_fields=["is_paid"])
        course_title = "All Courses Bundle"
    else:
        course = get_object_or_404(Course, slug=purchase.course_slug, is_published=True)
        enrollment, _ = Enrollment.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={"is_paid": True},
        )
        if not enrollment.is_paid:
            enrollment.is_paid = True
            enrollment.save(update_fields=["is_paid"])
        course_title = course.title

    try:
        subject = f"Payment received: {course_title}"
        user_name = purchase.purchaser_name or request.user.email
        text_body, html_body = get_payment_receipt_template(
            course_title=course_title,
            amount=str(purchase.amount_inr),
            order_id=order_id,
            payment_id=payment_id,
            user_name=user_name
        )
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@infosecdairies.io")
        _send_html_email(subject, text_body, html_body, request.user.email, from_email=from_email, context="payment_receipt")
    except Exception:
        logger.exception("Failed to send payment receipt email")

    return Response({"success": True, "course_slug": purchase.course_slug})


@api_view(["POST"])
@permission_classes([AllowAny])
def razorpay_webhook(request):
    """
    Razorpay calls this server-to-server when a payment is captured.
    Grants enrollment even if the frontend's verify_payment call failed.
    Configure in Razorpay dashboard → Webhooks → URL: /api/payments/webhook/
    Active event: payment.captured
    """
    webhook_secret = _clean_razorpay_cred(getattr(settings, "RAZORPAY_WEBHOOK_SECRET", ""))
    if not webhook_secret:
        logger.error("RAZORPAY_WEBHOOK_SECRET not configured — webhook ignored")
        return Response(status=400)

    body = request.body
    signature = request.headers.get("X-Razorpay-Signature", "")
    expected = hmac.new(webhook_secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        logger.warning("Razorpay webhook: invalid signature")
        return Response(status=400)

    event = request.data.get("event", "")
    if event != "payment.captured":
        return Response({"status": "ignored"})

    try:
        payment_entity = request.data["payload"]["payment"]["entity"]
        order_id = payment_entity.get("order_id")
        payment_id = payment_entity.get("id")
    except (KeyError, TypeError):
        return Response(status=400)

    if not order_id:
        return Response(status=400)

    purchase = CoursePurchase.objects.filter(razorpay_order_id=order_id).first()
    if not purchase:
        logger.warning("Razorpay webhook: unknown order_id=%s", order_id)
        return Response({"status": "unknown_order"})

    if purchase.status == CoursePurchase.STATUS_PAID:
        return Response({"status": "already_processed"})

    with transaction.atomic():
        purchase.status = CoursePurchase.STATUS_PAID
        purchase.razorpay_payment_id = payment_id
        purchase.paid_at = timezone.now()
        purchase.save(update_fields=["status", "razorpay_payment_id", "paid_at"])

        if purchase.course_slug == ALL_COURSES_BUNDLE_SLUG:
            for c in Course.objects.filter(is_published=True):
                enr, _ = Enrollment.objects.get_or_create(
                    user=purchase.user, course=c, defaults={"is_paid": True}
                )
                if not enr.is_paid:
                    enr.is_paid = True
                    enr.save(update_fields=["is_paid"])
        else:
            course = Course.objects.filter(
                slug=purchase.course_slug, is_published=True
            ).first()
            if course:
                enr, _ = Enrollment.objects.get_or_create(
                    user=purchase.user, course=course, defaults={"is_paid": True}
                )
                if not enr.is_paid:
                    enr.is_paid = True
                    enr.save(update_fields=["is_paid"])

    logger.info(
        "Razorpay webhook: enrollment granted user=%s course=%s order=%s payment=%s",
        purchase.user.email, purchase.course_slug, order_id, payment_id,
    )
    return Response({"status": "ok"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_purchases(request):
    """Return list of user's course purchases."""
    purchases = CoursePurchase.objects.filter(user=request.user).order_by("-created_at")
    data = [
        {
            "course_slug": p.course_slug,
            "status": p.status,
            "amount_inr": p.amount_inr,
            "paid_at": p.paid_at,
        }
        for p in purchases
    ]
    return Response(data)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_pricing(request):
    """
    GET /api/payments/pricing/?country=US
    Returns prices for all tiers in the visitor's local currency.
    Falls back to INR for unsupported countries.
    """
    country_code = (request.GET.get("country") or "IN").upper().strip()

    tiers = {
        "easy": 499,
        "medium": 799,
        "hard": 1199,
        "bundle": 3999,
    }

    sample = _get_local_price(country_code, "easy", 499)
    currency = sample["currency"]
    symbol = sample["symbol"]

    prices = {}
    for tier, inr_amount in tiers.items():
        result = _get_local_price(country_code, tier, inr_amount)
        prices[tier] = result["amount"]

    return Response({
        "country_code": country_code,
        "currency": currency,
        "symbol": symbol,
        "prices": prices,
    })
