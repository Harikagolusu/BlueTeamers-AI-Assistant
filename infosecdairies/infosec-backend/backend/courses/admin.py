from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Enrollment, LessonProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "is_published", "created_at")
    list_filter = ("level", "is_published")
    search_fields = ("title",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "is_paid", "promo_usage_count", "lesson_progress_count")
    list_filter = ("is_paid", "course")
    search_fields = ("user__email", "course__title")

    def promo_usage_count(self, obj):
        from payments.models import PromoCodeUsage
        count = PromoCodeUsage.objects.filter(user=obj.user, course_slug=obj.course.slug).count()
        return count
    promo_usage_count.short_description = "Promo Usages"

    def lesson_progress_count(self, obj):
        return LessonProgress.objects.filter(user=obj.user, course=obj.course).count()
    lesson_progress_count.short_description = "Lessons Done"


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "lesson_id", "completed_at")
    list_filter = ("course", "user")
    search_fields = ("user__email", "course__title", "lesson_id")
    ordering = ("-completed_at",)
