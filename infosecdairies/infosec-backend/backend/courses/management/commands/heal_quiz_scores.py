"""
Heals QuizScore records that were wrongly recorded as failed due to the
mis-generated quiz_answers.py (wrong correct-answer indices).

Every quiz submitted before the fix was scored against the wrong answer key,
so the database has passed=False / low score for users who actually passed
on the frontend.

This command sets passed=True, score=70 for every existing record that still
has passed=False, so no user has to retake anything.

Run once on the production server after deploying the quiz_answers.py fix:
    python manage.py heal_quiz_scores
    python manage.py heal_quiz_scores --dry-run   # preview without writing
"""
from django.core.management.base import BaseCommand
from courses.models import QuizScore


class Command(BaseCommand):
    help = "Heal wrong passed=False QuizScore records caused by the bad answer key"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print what would change without saving anything",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        qs = QuizScore.objects.filter(passed=False)
        total = qs.count()

        if total == 0:
            self.stdout.write(self.style.SUCCESS("Nothing to fix — no failed quiz records found."))
            return

        self.stdout.write(f"Found {total} failed quiz record(s) to heal.")

        if dry_run:
            for r in qs.order_by("user__email", "course_slug", "quiz_id"):
                self.stdout.write(
                    f"  [DRY RUN] would heal: user={r.user.email}  "
                    f"course={r.course_slug}  quiz={r.quiz_id}  "
                    f"score={r.score} -> 70  passed=False -> True"
                )
            self.stdout.write(self.style.WARNING(f"Dry run complete — {total} record(s) would be updated."))
            return

        updated = qs.update(passed=True, score=70)
        self.stdout.write(
            self.style.SUCCESS(
                f"Healed {updated} quiz record(s) — set passed=True, score=70."
            )
        )
