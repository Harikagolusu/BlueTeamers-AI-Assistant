"""Seed the local SQLite DB with a demo user and platform data for AI testing.

Creates/updates:
  - harika@example.com (password: password123), verified
  - Paid CoursePurchase + Enrollment for a few courses
  - LessonProgress for a subset of lessons per course
  - QuizScore records for one course

Run from the backend/ directory:
    ./.venv/bin/python seed_demo_user.py
"""
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.utils import timezone  # noqa: E402
from accounts.models import User  # noqa: E402
from courses.models import Course, Enrollment, LessonProgress, QuizScore  # noqa: E402
from payments.models import CoursePurchase  # noqa: E402

DEMO_EMAIL = "harika@example.com"
DEMO_PASSWORD = "password123"
DEMO_FULL_NAME = "Harika Demo User"

# slug -> completed lesson ids
SEED = {
    "blue-team-soc-fundamentals": ["1.1", "1.2", "1.3", "2.1", "2.2", "3.1"],
    "log-analysis-for-beginners": ["1.1", "1.2", "1.3", "2.1"],
    "siem-fundamentals": ["1.1", "1.2"],
}
QUIZ_SCORES = {
    "blue-team-soc-fundamentals": [("quiz-1", 80, True), ("quiz-2", 60, False)],
}

user, created = User.objects.get_or_create(email=DEMO_EMAIL)
if created:
    user.full_name = DEMO_FULL_NAME
    user.is_verified = True
    user.set_password(DEMO_PASSWORD)
    user.save()
    print(f"created user {DEMO_EMAIL}")
else:
    user.full_name = DEMO_FULL_NAME
    user.is_verified = True
    user.set_password(DEMO_PASSWORD)
    user.save()
    print(f"updated user {DEMO_EMAIL}")

for slug, lesson_ids in SEED.items():
    try:
        course = Course.objects.get(slug=slug)
    except Course.DoesNotExist:
        print(f"SKIP course not in DB: {slug}")
        continue

    enrollment, e_created = Enrollment.objects.get_or_create(user=user, course=course)
    if not enrollment.is_paid:
        enrollment.is_paid = True
        enrollment.save()
    print(f"enrolled (paid): {slug}")

    _, p_created = CoursePurchase.objects.get_or_create(
        user=user,
        course_slug=slug,
        defaults={
            "amount_inr": 799,
            "currency": "INR",
            "status": CoursePurchase.STATUS_PAID,
            "paid_at": timezone.now(),
            "razorpay_order_id": f"demo-order-{slug}",
            "razorpay_payment_id": f"demo-pay-{slug}",
        },
    )
    print(f"purchase {'created' if p_created else 'exists'}: {slug}")

    for lid in lesson_ids:
        _, lp_created = LessonProgress.objects.get_or_create(
            user=user, course=course, lesson_id=lid
        )
        print(f"  progress {'added' if lp_created else 'exists'}: {slug}/{lid}")

for slug, scores in QUIZ_SCORES.items():
    for quiz_id, score, passed in scores:
        qs, _ = QuizScore.objects.update_or_create(
            user=user,
            course_slug=slug,
            quiz_id=quiz_id,
            defaults={"score": score, "passed": passed},
        )
        print(f"quiz score set: {slug}/{quiz_id} = {score} passed={passed}")

print("DONE")
