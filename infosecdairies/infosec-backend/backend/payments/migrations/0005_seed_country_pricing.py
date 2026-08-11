from django.db import migrations


COUNTRY_PRICING = [
    ("AE", "AED", "AED"),
    ("GB", "GBP", "£"),
    ("KE", "KES", "KSh"),
    ("NG", "NGN", "₦"),
    ("PK", "PKR", "₨"),
    ("QA", "QAR", "QR"),
    ("SA", "SAR", "SR"),
    ("US", "USD", "$"),
]


def seed_country_pricing(apps, schema_editor):
    CountryPricing = apps.get_model("payments", "CountryPricing")
    for country_code, currency_code, symbol in COUNTRY_PRICING:
        CountryPricing.objects.get_or_create(
            country_code=country_code,
            defaults={
                "currency_code": currency_code,
                "currency_symbol": symbol,
                "is_active": True,
            },
        )


def unseed_country_pricing(apps, schema_editor):
    CountryPricing = apps.get_model("payments", "CountryPricing")
    CountryPricing.objects.filter(
        country_code__in=[c[0] for c in COUNTRY_PRICING]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0004_geo_pricing"),
    ]

    operations = [
        migrations.RunPython(seed_country_pricing, reverse_code=unseed_country_pricing),
    ]
