from django.core.management.base import BaseCommand
from payments.models import CoursePurchase
from courses.models import Course, Enrollment

ALL_COURSES_BUNDLE_SLUG = "all-courses-bundle"


class Command(BaseCommand):
    help = "Fix enrollments where CoursePurchase.status=paid but Enrollment.is_paid=False"

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show what would be fixed without writing")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        paid_purchases = CoursePurchase.objects.filter(status=CoursePurchase.STATUS_PAID).select_related("user")

        fixed_users = set()
        fixed_count = 0

        for purchase in paid_purchases:
            user = purchase.user
            if purchase.course_slug == ALL_COURSES_BUNDLE_SLUG:
                courses = list(Course.objects.filter(is_published=True))
            else:
                course = Course.objects.filter(slug=purchase.course_slug, is_published=True).first()
                courses = [course] if course else []

            for c in courses:
                enr = Enrollment.objects.filter(user=user, course=c).first()
                if enr and not enr.is_paid:
                    self.stdout.write(f"  FIX  user={user.email} course={c.slug}")
                    if not dry_run:
                        enr.is_paid = True
                        enr.save(update_fields=["is_paid"])
                    fixed_count += 1
                    fixed_users.add(user.email)
                elif not enr:
                    self.stdout.write(f"  CREATE  user={user.email} course={c.slug}")
                    if not dry_run:
                        Enrollment.objects.create(user=user, course=c, is_paid=True)
                    fixed_count += 1
                    fixed_users.add(user.email)

        label = "[DRY RUN] Would fix" if dry_run else "Fixed"
        self.stdout.write(self.style.SUCCESS(
            f"{label} {fixed_count} enrollment(s) across {len(fixed_users)} user(s)"
        ))
