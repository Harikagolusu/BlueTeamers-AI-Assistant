"""
Management command: import_lesson_content
─────────────────────────────────────────
Reads the pre-exported lesson content JSON and upserts every lesson into the
LessonContent table. Safe to re-run — existing records are updated in place.

Usage
─────
    python manage.py import_lesson_content
    python manage.py import_lesson_content --json-file /path/to/all_lessons.json
    python manage.py import_lesson_content --dry-run

The default JSON file path is:
    <repo>/infosec-backend/backend/courses/lesson_data/all_lessons.json

Deployment
──────────
Add this command to the Railway start script so content is always up-to-date:
    python manage.py migrate && python manage.py import_lesson_content && gunicorn ...
"""

import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from courses.models import LessonContent

# Default path: relative to this file → up 4 levels → lesson_data/all_lessons.json
_DEFAULT_JSON = (
    Path(__file__).resolve()
    .parent   # commands/
    .parent   # management/
    .parent   # courses/
    / "lesson_data"
    / "all_lessons.json"
)


class Command(BaseCommand):
    help = (
        "Import pre-exported lesson content JSON into the LessonContent table. "
        "Safe to re-run: upserts existing records."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--json-file",
            default=str(_DEFAULT_JSON),
            metavar="PATH",
            help=f"Path to the all_lessons.json export (default: {_DEFAULT_JSON})",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview what would be imported without writing to the database.",
        )
        parser.add_argument(
            "--course",
            metavar="SLUG",
            default=None,
            help="Import only lessons for a specific course slug (default: all courses).",
        )

    def handle(self, *args, **options):
        json_path = Path(options["json_file"])
        dry_run: bool = options["dry_run"]
        only_course: str | None = options["course"]

        if not json_path.exists():
            raise CommandError(
                f"Lesson content JSON not found at: {json_path}\n"
                "Run `npx tsx scripts/export_lesson_content.ts` first to generate it."
            )

        self.stdout.write(f"Reading: {json_path}")
        with open(json_path, "r", encoding="utf-8") as fh:
            data: dict[str, list[dict]] = json.load(fh)

        if not isinstance(data, dict):
            raise CommandError("JSON root must be an object mapping course_slug → [lesson, ...]")

        created = updated = skipped = 0
        courses_processed = []

        for course_slug, lessons in sorted(data.items()):
            if only_course and course_slug != only_course:
                continue

            if not isinstance(lessons, list):
                self.stderr.write(
                    self.style.WARNING(f"  Skipping {course_slug!r}: value is not a list")
                )
                continue

            courses_processed.append(course_slug)

            for lesson in lessons:
                lesson_id = lesson.get("id")
                if not lesson_id:
                    self.stderr.write(
                        self.style.WARNING(
                            f"  Skipping entry in {course_slug!r}: missing 'id' field"
                        )
                    )
                    skipped += 1
                    continue

                if dry_run:
                    self.stdout.write(f"  [dry-run] {course_slug}/{lesson_id}")
                    continue

                _obj, was_created = LessonContent.objects.update_or_create(
                    course_slug=course_slug,
                    lesson_id=lesson_id,
                    defaults={"content_json": lesson},
                )
                if was_created:
                    created += 1
                else:
                    updated += 1

        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f"\nDry-run complete — no changes made.\n"
                    f"Courses: {courses_processed}\n"
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"\nImport complete:\n"
                f"   Created : {created}\n"
                f"   Updated : {updated}\n"
                f"   Skipped : {skipped}\n"
                f"   Courses : {courses_processed}"
            )
        )
