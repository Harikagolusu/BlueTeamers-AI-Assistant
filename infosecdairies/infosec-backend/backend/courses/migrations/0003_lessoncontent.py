from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0002_quizscore"),
    ]

    operations = [
        migrations.CreateModel(
            name="LessonContent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "course_slug",
                    models.CharField(
                        db_index=True,
                        help_text="URL slug of the course (e.g. 'blue-team-soc-fundamentals')",
                        max_length=200,
                    ),
                ),
                (
                    "lesson_id",
                    models.CharField(
                        help_text="Lesson ID as used in the frontend routing (e.g. '1.1', 'la-2.3')",
                        max_length=100,
                    ),
                ),
                (
                    "content_json",
                    models.JSONField(
                        help_text="Full lesson payload: content, keyTakeaways, practicalExercise, additionalResources",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "unique_together": {("course_slug", "lesson_id")},
            },
        ),
        migrations.AddIndex(
            model_name="lessoncontent",
            index=models.Index(
                fields=["course_slug", "lesson_id"],
                name="lc_slug_lesson_idx",
            ),
        ),
    ]
