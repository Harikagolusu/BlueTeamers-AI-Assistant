from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.utils.html import escape
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import logging
import os
import uuid
import base64

from accounts.email_templates import _send_html_email, get_certificate_template
from .models import Certificate

logger = logging.getLogger(__name__)


def _rate_limit(key, limit, period_seconds):
    """Returns True if caller exceeded the limit."""
    count = cache.get(key, 0)
    if count >= limit:
        return True
    cache.set(key, count + 1, period_seconds)
    return False


def _completion_date_for(user, course):
    """Return ISO date string of when user last completed a lesson/quiz for this course."""
    from courses.models import LessonProgress, QuizScore
    lp = LessonProgress.objects.filter(user=user, course=course).order_by('-completed_at').first()
    if lp:
        return str(lp.completed_at.date())
    qs = QuizScore.objects.filter(user=user, course_slug=course.slug, passed=True).order_by('-submitted_at').first()
    if qs:
        return str(qs.submitted_at.date())
    return str(timezone.now().date())


@api_view(["GET"])
def lookup_certificate(request, cert_id):
    """Lookup certificate by ID."""
    ip = (request.META.get("HTTP_X_FORWARDED_FOR", "") or request.META.get("REMOTE_ADDR", "unknown")).split(",")[0].strip()
    if _rate_limit(f"cert_lookup:{ip}", 30, 3600):
        return JsonResponse({"error": "Rate limit exceeded. Try again later."}, status=429)
    try:
        certificate = Certificate.objects.get(cert_id=cert_id)
        return JsonResponse({
            'success': True,
            'certId': certificate.cert_id,
            'studentName': certificate.student_name,
            'courseName': certificate.course_name,
            'issueDate': certificate.issue_date,
            'verified': True,
        })
    except Certificate.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Certificate not found'}, status=404)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_certificate(request, slug):
    """
    Return this user's certificate for the given course slug (if it exists),
    or the server-computed completion date + current name (for first-time generation).
    Always returns studentName and issueDate so the client can draw the canvas
    with the correct frozen values.
    """
    from courses.models import Course

    ip = (request.META.get("HTTP_X_FORWARDED_FOR", "") or request.META.get("REMOTE_ADDR", "unknown")).split(",")[0].strip()
    if _rate_limit(f"cert_my:{ip}:{request.user.id}", 60, 3600):
        return JsonResponse({"error": "Rate limit exceeded."}, status=429)

    # If cert already exists, return the frozen stored values
    existing = Certificate.objects.filter(user=request.user, course_slug=slug).first()
    if existing:
        return JsonResponse({
            'exists': True,
            'certId': existing.cert_id,
            'studentName': existing.student_name,
            'issueDate': existing.issue_date,
            'courseName': existing.course_name,
        })

    # Cert not yet generated — return completion date so client uses the right date
    try:
        course = Course.objects.get(slug=slug, is_published=True)
        completion_date = _completion_date_for(request.user, course)
    except Course.DoesNotExist:
        completion_date = str(timezone.now().date())

    return JsonResponse({
        'exists': False,
        'studentName': request.user.full_name or request.user.email,
        'issueDate': completion_date,
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_certificate(request):
    """
    SECURITY: Requires JWT authentication + paid enrollment + server-side quiz completion.
    - user_email in the body is IGNORED — always uses the authenticated user's email.
    - course_slug must be a course the user is enrolled in and has paid for.
    - User must have at least one passing QuizScore for the course.
    - If a cert already exists for this user+course, returns the existing one (no re-upload).
    - issue_date is taken from server-side completion records, never from the client.
    - student_name is frozen from the DB at generation time (username changes have no effect).
    """
    from courses.models import Course, Enrollment, QuizScore

    image_data = request.data.get('image')
    course_slug = (request.data.get('course_slug') or '').strip()
    user_email = request.user.email

    if not image_data:
        return JsonResponse({'error': 'No image data provided'}, status=400)
    if not course_slug:
        return JsonResponse({'error': 'course_slug is required'}, status=400)

    FREE_SLUG = "network-fundamentals"

    # If cert already exists, return it immediately — no rate limit consumed for re-downloads
    existing = Certificate.objects.filter(user=request.user, course_slug=course_slug).first()
    if existing:
        return JsonResponse({
            'success': True,
            'cert_id': existing.cert_id,
            'issue_date': existing.issue_date,
            'student_name': existing.student_name,
            'already_exists': True,
        })

    if _rate_limit(f"cert_upload:{request.user.id}", 5, 3600):
        return JsonResponse({"error": "Too many certificate requests. Try again later."}, status=429)

    try:
        course = Course.objects.get(slug=course_slug, is_published=True)
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

    # Verify paid enrollment (free course exempt)
    if course_slug != FREE_SLUG:
        enrolled = Enrollment.objects.filter(
            user=request.user, course=course, is_paid=True
        ).exists()
        if not enrolled:
            return JsonResponse(
                {'error': 'You must be enrolled and have paid for this course to earn a certificate'},
                status=403,
            )

    # Verify server-side quiz completion
    has_passing_score = QuizScore.objects.filter(
        user=request.user,
        course_slug=course_slug,
        passed=True,
    ).exists()
    if not has_passing_score:
        return JsonResponse(
            {'error': 'You must pass at least one quiz to earn this certificate'},
            status=403,
        )

    # Completion date from server records — never trust the client
    completion_date = _completion_date_for(request.user, course)

    # Freeze name at generation time — username changes after this have no effect
    frozen_name = request.user.full_name or user_email

    # Process image
    try:
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        image_bytes = base64.b64decode(image_data)
    except Exception:
        return JsonResponse({'error': 'Invalid image data'}, status=400)

    filename = (
        f"certificates/{course_slug}_"
        f"{user_email.replace('@', '_').replace('.', '_')}_"
        f"{uuid.uuid4().hex[:8]}.png"
    )
    path = default_storage.save(filename, ContentFile(image_bytes))
    public_url = default_storage.url(path)

    if not (public_url.startswith("http://") or public_url.startswith("https://")):
        if not public_url.startswith("/"):
            public_url = f"/{public_url}"
        public_url = f"{request.scheme}://{request.get_host()}{public_url}"

    cert_id = uuid.uuid4().hex[:16]
    Certificate.objects.create(
        cert_id=cert_id,
        user=request.user,
        course_slug=course_slug,
        student_name=frozen_name,
        course_name=course.title,
        issue_date=completion_date,
        image_url=public_url,
    )

    try:
        subject = "Your certificate is ready"
        text_body, html_body = get_certificate_template(
            download_url=public_url,
            course_name=course_slug.replace('-', ' ').title()
        )
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@infosecdairies.io")
        _send_html_email(subject, text_body, html_body, user_email, from_email=from_email, context="certificate")
    except Exception:
        logger.exception("Failed to send certificate email")

    return JsonResponse({
        'success': True,
        'url': public_url,
        'path': path,
        'cert_id': cert_id,
        'issue_date': completion_date,
        'student_name': frozen_name,
    })


def certificate_share(request):
    img = request.GET.get("img") or ""
    course = request.GET.get("course") or "Course"
    name = request.GET.get("name") or "Student"
    date = request.GET.get("date") or ""

    safe_name = escape(name)
    safe_course = escape(course)
    safe_date = escape(date)

    title = f"{safe_name} completed {safe_course}"
    description = f"Certificate of completion for {safe_course} at Infosec Dairies."
    if date:
        description = f"Certificate of completion for {safe_course} at Infosec Dairies ({safe_date})."

    if not (img.startswith("http://") or img.startswith("https://")):
        img = ""

    page_url = request.build_absolute_uri()

    og_image_meta = f'<meta property="og:image" content="{escape(img)}" />' if img else ""
    twitter_image_meta = f'<meta name="twitter:image" content="{escape(img)}" />' if img else ""

    html = f"""<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>{title}</title>
    <meta property=\"og:site_name\" content=\"Infosec Dairies\" />
    <meta property=\"og:title\" content=\"{title}\" />
    <meta property=\"og:description\" content=\"{description}\" />
    <meta property=\"og:type\" content=\"website\" />
    <meta property=\"og:url\" content=\"{escape(page_url)}\" />
    {og_image_meta}
    <meta name=\"twitter:card\" content=\"summary_large_image\" />
    <meta name=\"twitter:title\" content=\"{title}\" />
    <meta name=\"twitter:description\" content=\"{description}\" />
    {twitter_image_meta}
    <meta http-equiv=\"refresh\" content=\"0; url=https://www.infosecdairies.io/\" />
  </head>
  <body></body>
</html>"""

    return HttpResponse(html, content_type="text/html")
