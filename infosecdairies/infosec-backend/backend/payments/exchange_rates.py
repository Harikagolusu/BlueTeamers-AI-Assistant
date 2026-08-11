import math
import logging
import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_KEY = "inr_exchange_rates"
CACHE_TTL = 3600  # 1 hour

FALLBACK_RATES = {
    "USD": 0.012, "GBP": 0.0095, "EUR": 0.011,
    "PKR": 3.32,  "SAR": 0.045, "AED": 0.044,
    "QAR": 0.044, "KES": 1.55,  "NGN": 19.5,
}

# Map ISO alpha-2 country code → (currency_code, currency_symbol)
COUNTRY_CURRENCY_MAP = {
    "US": ("USD", "$"),
    "GB": ("GBP", "£"),
    "PK": ("PKR", "₨"),
    "SA": ("SAR", "SR"),
    "AE": ("AED", "AED"),
    "QA": ("QAR", "QR"),
    "KE": ("KES", "KSh"),
    "NG": ("NGN", "₦"),
}


def get_rates() -> dict:
    """Return dict of {currency_code: rate_per_1_INR}. Falls back to hardcoded rates on failure."""
    cached = cache.get(CACHE_KEY)
    if cached:
        return cached

    try:
        resp = requests.get("https://open.er-api.com/v6/latest/INR", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        if data.get("result") == "success":
            rates = data.get("rates") or {}
            if not rates:
                return FALLBACK_RATES
            cache.set(CACHE_KEY, rates, CACHE_TTL)
            return rates
    except Exception:
        logger.warning("Failed to fetch exchange rates, using fallback", exc_info=True)

    return FALLBACK_RATES


def inr_to_currency(amount_inr: int, currency_code: str) -> float:
    """Convert an INR integer amount to foreign currency, rounded to X.99 format."""
    if currency_code == "INR":
        return float(amount_inr)
    rates = get_rates()
    rate = rates.get(currency_code)
    if rate is None:
        return float(amount_inr)
    converted = amount_inr * rate
    return round_to_99(converted)


def round_to_99(amount: float) -> float:
    """Round 9.73 → 9.99, 12.45 → 12.99, 44.20 → 44.99.
    # 12.0 → 11.99 by design — all prices land at X.99
    """
    if amount <= 0:
        return 0.0
    return float(math.ceil(amount)) - 0.01
