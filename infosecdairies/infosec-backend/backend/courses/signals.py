from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Enrollment, LessonProgress


@receiver(post_delete, sender=Enrollment)
def cleanup_on_enrollment_delete(sender, instance, **kwargs):
    """When an enrollment is removed, wipe the user's promo usage and lesson progress for that course."""
    from payments.models import PromoCodeUsage

    PromoCodeUsage.objects.filter(
        user=instance.user,
        course_slug=instance.course.slug,
    ).delete()

    LessonProgress.objects.filter(
        user=instance.user,
        course=instance.course,
    ).delete()
