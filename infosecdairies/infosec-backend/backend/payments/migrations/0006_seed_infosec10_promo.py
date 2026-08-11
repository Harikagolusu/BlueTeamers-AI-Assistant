from django.db import migrations


def seed_infosec10(apps, schema_editor):
    PromoCode = apps.get_model("payments", "PromoCode")
    PromoCode.objects.get_or_create(
        code="INFOSEC10",
        course_slug="all",
        defaults={
            "discount_percent": 50,
            "max_uses": 0,
            "is_active": True,
        },
    )


def remove_infosec10(apps, schema_editor):
    PromoCode = apps.get_model("payments", "PromoCode")
    PromoCode.objects.filter(code="INFOSEC10", course_slug="all").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0005_seed_country_pricing"),
    ]

    operations = [
        migrations.RunPython(seed_infosec10, remove_infosec10),
    ]
