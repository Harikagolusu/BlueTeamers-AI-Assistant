from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    level = models.CharField(max_length=50)
    duration_hours = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self) -> str:  # type: ignore[override]
        return f"{self.user.email} -> {self.course.slug}"


class LessonProgress(models.Model):
    """Tracks which lessons a user has completed within a course."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_id = models.CharField(max_length=50)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course", "lesson_id")

    def __str__(self) -> str:  # type: ignore[override]
        return f"{self.user.email} -> {self.course.slug} -> {self.lesson_id}"


class QuizScore(models.Model):
    """Server-authoritative record of a quiz attempt. Best score per (user, course, quiz) is kept."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_slug = models.CharField(max_length=200, db_index=True)
    quiz_id = models.CharField(max_length=100)
    score = models.PositiveIntegerField()
    passed = models.BooleanField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course_slug", "quiz_id")
        indexes = [
            models.Index(fields=["user", "course_slug"]),
        ]

    def __str__(self) -> str:  # type: ignore[override]
        return f"{self.user.email} -> {self.course_slug}/{self.quiz_id}: {self.score}%"


class LessonContent(models.Model):
    """
    Server-authoritative lesson content (markdown text, key takeaways, exercises, resources).

    Security model
    ─────────────
    Content is NEVER bundled into the frontend JS. It is served only to authenticated,
    enrolled, and (for paid courses) paid users via GET /api/courses/{slug}/lessons/{id}/content/.
    This prevents bundle-extraction attacks where an attacker downloads the Vite JS
    bundle and reads every lesson without a paid account.

    Populated by:  python manage.py import_lesson_content
    """
    course_slug = models.CharField(
        max_length=200,
        db_index=True,
        help_text="URL slug of the course (e.g. 'blue-team-soc-fundamentals')",
    )
    lesson_id = models.CharField(
        max_length=100,
        help_text="Lesson ID as used in the frontend routing (e.g. '1.1', 'la-2.3')",
    )
    content_json = models.JSONField(
        help_text="Full lesson payload: content, keyTakeaways, practicalExercise, additionalResources",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("course_slug", "lesson_id")
        indexes = [
            models.Index(fields=["course_slug", "lesson_id"], name="lc_slug_lesson_idx"),
        ]

    def __str__(self) -> str:  # type: ignore[override]
        return f"{self.course_slug}/{self.lesson_id}"
