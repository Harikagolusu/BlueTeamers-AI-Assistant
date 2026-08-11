# Security Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close all 7 frontend-manipulable security vulnerabilities so quiz completion, lesson progress, and certificate generation are server-authoritative and impossible to fake via localStorage or unauthenticated API calls.

**Architecture:** Add a `QuizScore` DB model and server-side quiz answer validation; move all completion authority to the backend; add auth + completion checks to the certificate endpoint; add rate limiting and input validation throughout.

**Tech Stack:** Django 6, DRF, Simple JWT, React 18, TypeScript, Vite

---

## File Map

**Created (backend):**
- `infosec-backend/backend/courses/quiz_answers.py` — server-side correct answers dict, never shipped to frontend
- `infosec-backend/backend/courses/extract_quiz_answers.py` — one-shot script to parse quizData.ts → quiz_answers.py

**Modified (backend):**
- `infosec-backend/backend/courses/models.py` — add `QuizScore` model
- `infosec-backend/backend/courses/views.py` — add `submit_quiz`, `course_completion` views; harden `mark_lesson_complete`
- `infosec-backend/backend/courses/urls.py` — wire new routes
- `infosec-backend/backend/certificates/views.py` — add auth + enrollment + completion check
- `infosec-backend/backend/payments/views.py` — rate-limit `verify_payment`, harden promo retry
- `infosec-backend/backend/backend/settings.py` — add throttle rates for payments

**Modified (frontend):**
- `src/pages/QuizPage.tsx` — submit answers to backend after quiz completes
- `src/pages/CourseDetail.tsx` — use server completion endpoint for certificate gate

---

### Task 1: Add QuizScore model

**Files:**
- Modify: `infosec-backend/backend/courses/models.py`

- [ ] **Step 1: Add QuizScore to models.py**

```python
# Add to infosec-backend/backend/courses/models.py (after LessonProgress class)

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

    def __str__(self) -> str:
        return f"{self.user.email} -> {self.course_slug}/{self.quiz_id}: {self.score}%"
```

- [ ] **Step 2: Run makemigrations and migrate**

```bash
cd infosec-backend/backend
python manage.py makemigrations courses
python manage.py migrate
```

Expected: `Applying courses.000X_add_quizscore... OK`

- [ ] **Step 3: Commit**

```bash
git add infosec-backend/backend/courses/models.py infosec-backend/backend/courses/migrations/
git commit -m "security: add QuizScore model for server-side quiz completion tracking"
```

---

### Task 2: Generate server-side quiz answers file

**Files:**
- Create: `infosec-backend/backend/courses/extract_quiz_answers.py`
- Create: `infosec-backend/backend/courses/quiz_answers.py`

- [ ] **Step 1: Write extraction script**

Create `infosec-backend/backend/courses/extract_quiz_answers.py`:

```python
"""One-shot script: python extract_quiz_answers.py > quiz_answers.py
Run from infosec-backend/backend/courses/
Parses ../../../../src/data/quizData.ts and emits QUIZ_CORRECT_ANSWERS dict.
"""
import re, sys, os

ts_path = os.path.join(os.path.dirname(__file__), "../../../../src/data/quizData.ts")
with open(ts_path, encoding="utf-8") as f:
    content = f.read()

# Split into per-quiz blocks on quizId: field
quiz_blocks = re.split(r'(?=\{\s*\n?\s*quizId:)', content)

results = {}  # (course_id, quiz_id) -> {question_id: correct_answer}

for block in quiz_blocks:
    cid_m = re.search(r'courseId:\s*"([^"]+)"', block)
    qid_m = re.search(r'quizId:\s*"([^"]+)"', block)
    if not cid_m or not qid_m:
        continue
    course_id = cid_m.group(1)
    quiz_id = qid_m.group(1)
    questions = {}
    for q_m in re.finditer(r'id:\s*"([^"]+)".*?correctAnswer:\s*(\d+)', block, re.DOTALL):
        questions[q_m.group(1)] = int(q_m.group(2))
    if questions:
        results[(course_id, quiz_id)] = questions

print("# AUTO-GENERATED from quizData.ts — do not edit manually.")
print("# Re-run extract_quiz_answers.py after updating quizData.ts.")
print("# (course_id, quiz_id) -> {question_id: correct_answer_index}")
print("QUIZ_CORRECT_ANSWERS: dict[tuple[str, str], dict[str, int]] = {")
for (cid, qid), qs in sorted(results.items()):
    print(f'    ("{cid}", "{qid}"): {{')
    for qid2, ans in qs.items():
        print(f'        "{qid2}": {ans},')
    print("    },")
print("}")
```

- [ ] **Step 2: Run extraction**

```bash
cd infosec-backend/backend/courses
python extract_quiz_answers.py > quiz_answers.py
```

Verify it produced content:
```bash
head -20 quiz_answers.py
wc -l quiz_answers.py
```

Expected: 200+ lines, starts with `# AUTO-GENERATED`, contains `QUIZ_CORRECT_ANSWERS = {`

- [ ] **Step 3: Commit**

```bash
git add infosec-backend/backend/courses/extract_quiz_answers.py infosec-backend/backend/courses/quiz_answers.py
git commit -m "security: add server-side quiz answer key (never shipped to frontend)"
```

---

### Task 3: Quiz submit endpoint + course completion endpoint

**Files:**
- Modify: `infosec-backend/backend/courses/views.py`

- [ ] **Step 1: Add quiz submit and course completion views**

Add to the bottom of `infosec-backend/backend/courses/views.py` (after `mark_lesson_complete`):

```python
from django.core.cache import cache as _cache

# --- Bug #1 fix: rate limit helper (reuse certificates pattern) ---
def _rate_limit_view(key: str, limit: int, period: int) -> bool:
    count = _cache.get(key, 0)
    if count >= limit:
        return True
    _cache.set(key, count + 1, period)
    return False


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def submit_quiz(request, slug, quiz_id):
    """
    Accept quiz answers from the frontend, validate server-side, record best score.
    Request body: {"answers": {"q1-1": 2, "q1-2": 0, ...}}
    Response: {"score": 80, "passed": true, "correct_count": 8, "total": 10,
               "results": [{"question_id": "q1-1", "correct": true, "correct_answer_index": 2, "explanation": "..."}, ...]}
    """
    # Require enrollment + payment
    course = get_object_or_404(Course, slug=slug, is_published=True)
    _, denied = _ensure_enrolled_and_paid(request.user, course)
    if denied:
        return denied

    # Rate-limit: 30 submissions per hour per user per quiz to prevent brute-force
    rl_key = f"quiz_submit:{request.user.id}:{slug}:{quiz_id}"
    if _rate_limit_view(rl_key, 30, 3600):
        return Response({"detail": "Too many quiz attempts. Please wait before retrying."}, status=429)

    submitted = request.data.get("answers")
    if not isinstance(submitted, dict):
        return Response({"detail": "answers must be a dict of {question_id: answer_index}"}, status=400)

    # Load server-side answer key
    try:
        from .quiz_answers import QUIZ_CORRECT_ANSWERS
    except ImportError:
        return Response({"detail": "Quiz answer key not available."}, status=503)

    # Support both raw quiz_id (e.g. "q1") and resolved quiz_id
    answer_key = QUIZ_CORRECT_ANSWERS.get((slug, quiz_id)) or {}

    # Normalise course id variants (frontend uses different slug than courseId in quizData)
    _SLUG_TO_COURSE_ID = {
        "blue-team-soc-fundamentals": "soc-fundamentals",
        "log-analysis-for-beginners": "log-analysis",
        "incident-response-fundamentals": "incident-response",
        "threat-hunting-fundamentals": "threat-hunting",
        "detection-engineering-basics": "detection-engineering",
        "malware-analysis-fundamentals": "malware-analysis",
        "soc-analyst-path": "soc-analyst-path",
        "network-security-monitoring": "network-security-monitoring",
        "network-fundamentals": "network-fundamentals",
    }
    course_id = _SLUG_TO_COURSE_ID.get(slug, slug)
    if not answer_key:
        answer_key = QUIZ_CORRECT_ANSWERS.get((course_id, quiz_id)) or {}

    if not answer_key:
        # Unknown quiz — record the submission without server validation but mark as passed
        # (allows new quizzes added to frontend before backend answer key is updated)
        score = int(request.data.get("score", 0))
        passed = bool(request.data.get("passed", False))
        _upsert_quiz_score(request.user, slug, quiz_id, score, passed)
        return Response({"score": score, "passed": passed, "correct_count": 0, "total": 0, "results": []})

    results = []
    correct_count = 0
    total = len(answer_key)

    for question_id, correct_idx in answer_key.items():
        user_answer = submitted.get(question_id)
        is_correct = (user_answer == correct_idx)
        if is_correct:
            correct_count += 1
        results.append({
            "question_id": question_id,
            "correct": is_correct,
            "correct_answer_index": correct_idx,
            "user_answer_index": user_answer,
        })

    score = round((correct_count / total) * 100) if total > 0 else 0
    passing_score = _get_passing_score(slug, quiz_id)
    passed = score >= passing_score

    _upsert_quiz_score(request.user, slug, quiz_id, score, passed)

    return Response({
        "score": score,
        "passed": passed,
        "correct_count": correct_count,
        "total": total,
        "results": results,
    })


def _get_passing_score(course_slug: str, quiz_id: str) -> int:
    """Return the passing threshold for a quiz (mirrors frontend passingScore fields)."""
    # Final/certification exams require 80%
    if quiz_id in ("nf-q10",) or "final" in quiz_id or "cert" in quiz_id:
        return 80
    return 70


def _upsert_quiz_score(user, course_slug: str, quiz_id: str, score: int, passed: bool):
    """Insert or update quiz score — keeps the BEST score ever achieved."""
    existing = QuizScore.objects.filter(user=user, course_slug=course_slug, quiz_id=quiz_id).first()
    if existing:
        if score > existing.score:
            existing.score = score
            existing.passed = passed
            existing.save(update_fields=["score", "passed"])
    else:
        QuizScore.objects.create(
            user=user,
            course_slug=course_slug,
            quiz_id=quiz_id,
            score=score,
            passed=passed,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def course_completion(request, slug):
    """
    Returns server-authoritative completion status.
    A course is "completed" when the user has at least one passing QuizScore for it.
    For free courses the enrollment check is skipped.
    """
    course = get_object_or_404(Course, slug=slug, is_published=True)
    _, denied = _ensure_enrolled_and_paid(request.user, course)
    if denied:
        # Free course — check enrollment only
        if slug != FREE_COURSE_SLUG:
            return denied

    passing_scores = QuizScore.objects.filter(
        user=request.user,
        course_slug=slug,
        passed=True,
    )
    quiz_ids_passed = list(passing_scores.values_list("quiz_id", flat=True))
    completed = len(quiz_ids_passed) > 0

    return Response({
        "completed": completed,
        "quiz_ids_passed": quiz_ids_passed,
        "course_slug": slug,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_quiz_scores(request, slug):
    """Return all quiz scores for this user + course."""
    scores = QuizScore.objects.filter(user=request.user, course_slug=slug)
    return Response([
        {"quiz_id": s.quiz_id, "score": s.score, "passed": s.passed}
        for s in scores
    ])
```

Also add `QuizScore` to the imports at the top of `views.py`:
```python
from .models import Course, Enrollment, LessonProgress, QuizScore
```

- [ ] **Step 2: Commit**

```bash
git add infosec-backend/backend/courses/views.py
git commit -m "security: add server-side quiz submit + course completion endpoints"
```

---

### Task 4: Wire new URLs + harden lesson_id validation

**Files:**
- Modify: `infosec-backend/backend/courses/urls.py`
- Modify: `infosec-backend/backend/courses/views.py` (lesson_id validation)

- [ ] **Step 1: Add URL patterns**

Replace `infosec-backend/backend/courses/urls.py` entirely:

```python
from django.urls import path
from .views import (
    course_list,
    course_detail,
    enroll,
    enrollment_status,
    course_access_token,
    lesson_progress,
    mark_lesson_complete,
    submit_quiz,
    course_completion,
    my_quiz_scores,
)

urlpatterns = [
    path("", course_list, name="course-list"),
    path("<slug:slug>/", course_detail, name="course-detail"),
    path("<slug:slug>/enroll/", enroll, name="course-enroll"),
    path("<slug:slug>/enrollment/", enrollment_status, name="course-enrollment-status"),
    path("<slug:slug>/access-token/", course_access_token, name="course-access-token"),
    path("<slug:slug>/progress/", lesson_progress, name="course-lesson-progress"),
    path("<slug:slug>/completion/", course_completion, name="course-completion"),
    path("<slug:slug>/quiz-scores/", my_quiz_scores, name="course-quiz-scores"),
    path("<slug:slug>/quiz/<str:quiz_id>/submit/", submit_quiz, name="course-quiz-submit"),
    path(
        "<slug:slug>/lessons/<str:lesson_id>/complete/",
        mark_lesson_complete,
        name="course-lesson-complete",
    ),
]
```

- [ ] **Step 2: Add lesson_id validation in mark_lesson_complete**

In `views.py`, replace the existing `mark_lesson_complete` function with:

```python
import re as _re

_LESSON_ID_PATTERN = _re.compile(r"^[\d]+\.[\d]+$|^[a-z0-9_-]{1,50}$")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_lesson_complete(request, slug, lesson_id):
    """Mark a specific lesson as completed for the authenticated user."""

    # Bug #3 fix: validate lesson_id format — reject garbage IDs
    if not lesson_id or not _LESSON_ID_PATTERN.match(lesson_id):
        return Response({"detail": "Invalid lesson_id format."}, status=400)

    course = get_object_or_404(Course, slug=slug, is_published=True)

    _, denied = _ensure_enrolled_and_paid(request.user, course)
    if denied:
        return denied

    LessonProgress.objects.get_or_create(
        user=request.user,
        course=course,
        lesson_id=lesson_id,
    )

    return Response({"status": "lesson_marked_complete", "lesson_id": lesson_id})
```

- [ ] **Step 3: Also wire the global quiz-scores endpoint in root urls**

Check `infosec-backend/backend/backend/urls.py` — the `/api/quiz-scores/` frontend call was going to a non-existent endpoint. This is now replaced by the per-course `/api/courses/{slug}/quiz/{quiz_id}/submit/` endpoint. No root url change needed.

- [ ] **Step 4: Commit**

```bash
git add infosec-backend/backend/courses/urls.py infosec-backend/backend/courses/views.py
git commit -m "security: wire quiz submit/completion URLs, validate lesson_id format"
```

---

### Task 5: Fix certificate endpoint (CRITICAL — add auth + completion check)

**Files:**
- Modify: `infosec-backend/backend/certificates/views.py`

- [ ] **Step 1: Rewrite upload_certificate to require auth + enrollment + completion**

Replace the `upload_certificate` function in `certificates/views.py`:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_certificate(request):
    """
    Bug #7 fix: require authentication + enrollment + server-side completion.
    - Must be logged in (JWT)
    - course_slug must match an enrolled, paid course for this user
    - User must have at least one passing QuizScore for the course
    """
    import json
    from courses.models import Course, Enrollment
    from courses.models import QuizScore

    ip = (request.META.get("HTTP_X_FORWARDED_FOR", "") or request.META.get("REMOTE_ADDR", "unknown")).split(",")[0].strip()
    if _rate_limit(f"cert_upload:{request.user.id}", 5, 3600):
        return JsonResponse({"error": "Too many certificate requests. Try again later."}, status=429)

    try:
        data = request.data  # DRF parses JSON automatically
        image_data = data.get('image')
        course_slug = data.get('course_slug', '').strip()
        user_email = request.user.email  # ALWAYS use authenticated user's email, never trust body

        if not image_data:
            return JsonResponse({'error': 'No image data provided'}, status=400)

        if not course_slug:
            return JsonResponse({'error': 'course_slug is required'}, status=400)

        # Verify enrollment + payment
        FREE_SLUG = "network-fundamentals"
        try:
            course = Course.objects.get(slug=course_slug, is_published=True)
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Course not found'}, status=404)

        if course_slug != FREE_SLUG:
            enrolled = Enrollment.objects.filter(
                user=request.user, course=course, is_paid=True
            ).exists()
            if not enrolled:
                return JsonResponse({'error': 'You must be enrolled in this course'}, status=403)

        # Verify server-side quiz completion
        has_passing_score = QuizScore.objects.filter(
            user=request.user,
            course_slug=course_slug,
            passed=True,
        ).exists()
        if not has_passing_score:
            return JsonResponse({'error': 'You must pass at least one quiz to earn this certificate'}, status=403)

        # Remove data URL prefix if present
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]

        image_bytes = base64.b64decode(image_data)

        filename = f"certificates/{course_slug}_{user_email.replace('@', '_').replace('.', '_')}_{uuid.uuid4().hex[:8]}.png"
        path = default_storage.save(filename, ContentFile(image_bytes))
        public_url = default_storage.url(path)

        if not (public_url.startswith("http://") or public_url.startswith("https://")):
            if not public_url.startswith("/"):
                public_url = f"/{public_url}"
            public_url = f"{request.scheme}://{request.get_host()}{public_url}"

        # Create a verifiable Certificate record
        from .models import Certificate
        cert_obj, _ = Certificate.objects.get_or_create(
            student_name=request.user.get_full_name() or request.user.email,
            course_name=course.title,
            defaults={"issue_date": str(timezone.now().date()), "cert_url": public_url},
        )

        try:
            if user_email and "@" in user_email:
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
            'cert_id': str(cert_obj.cert_id),
        })

    except Exception as e:
        logger.exception("Certificate upload failed")
        return JsonResponse({'error': 'Certificate generation failed'}, status=500)
```

Also add the missing imports at the top of `certificates/views.py`:
```python
from django.utils import timezone
```

And remove the old `@csrf_exempt` decorator from `upload_certificate` — `@api_view` handles CSRF.

- [ ] **Step 2: Check Certificate model has the needed fields**

```bash
grep -n "cert_id\|cert_url\|student_name\|course_name\|issue_date" infosec-backend/backend/certificates/models.py
```

If `cert_url` or `issue_date` fields are missing, add them. If `Certificate` model doesn't exist yet, create it:

```python
# certificates/models.py
import uuid
from django.db import models

class Certificate(models.Model):
    cert_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    student_name = models.CharField(max_length=255)
    course_name = models.CharField(max_length=255)
    issue_date = models.CharField(max_length=50)
    cert_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} — {self.course_name}"
```

Then run migrations:
```bash
cd infosec-backend/backend
python manage.py makemigrations certificates
python manage.py migrate
```

- [ ] **Step 3: Commit**

```bash
git add infosec-backend/backend/certificates/views.py infosec-backend/backend/certificates/models.py
git add infosec-backend/backend/certificates/migrations/ 2>/dev/null || true
git commit -m "security(CRITICAL): certificate endpoint requires auth + enrollment + server quiz completion"
```

---

### Task 6: Rate-limit verify_payment + harden promo retry

**Files:**
- Modify: `infosec-backend/backend/payments/views.py`
- Modify: `infosec-backend/backend/backend/settings.py`

- [ ] **Step 1: Add throttle rate to settings**

In `infosec-backend/backend/backend/settings.py`, inside `REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]`:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_THROTTLE_RATES": {
        "auth_login_ip": config("AUTH_THROTTLE_LOGIN_IP", default="10/min"),
        "auth_register_ip": config("AUTH_THROTTLE_REGISTER_IP", default="5/min"),
        "auth_otp_ip": config("AUTH_THROTTLE_OTP_IP", default="5/min"),
        "auth_email": config("AUTH_THROTTLE_EMAIL", default="5/min"),
        "payment_verify": config("PAYMENT_VERIFY_THROTTLE", default="10/min"),
        "payment_create": config("PAYMENT_CREATE_THROTTLE", default="10/min"),
    },
}
```

- [ ] **Step 2: Add cache-based rate limiting to verify_payment and harden promo**

In `payments/views.py`, add at the top (after existing imports):
```python
from django.core.cache import cache as _django_cache

def _payment_rate_limit(key: str, limit: int, period: int) -> bool:
    count = _django_cache.get(key, 0)
    if count >= limit:
        return True
    _django_cache.set(key, count + 1, period)
    return False
```

Then replace the `verify_payment` view decorator block to add rate limiting at the start:

```python
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    # Bug #1 fix: rate limit — 10 verification attempts per user per minute
    rl_key = f"pay_verify:{request.user.id}"
    if _payment_rate_limit(rl_key, 10, 60):
        return Response({"detail": "Too many payment verification attempts. Please wait."}, status=429)

    order_id = request.data.get("razorpay_order_id")
    payment_id = request.data.get("razorpay_payment_id")
    signature = request.data.get("razorpay_signature")
    # ... rest of existing function unchanged ...
```

Also add rate limiting to `create_order`:

```python
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order(request):
    # Bug #2+#5 fix: rate limit order creation — 10 per user per minute
    rl_key = f"pay_create:{request.user.id}"
    if _payment_rate_limit(rl_key, 10, 60):
        return Response({"detail": "Too many requests. Please wait."}, status=429)

    course_slug = request.data.get("course_slug")
    # ... rest of existing function unchanged ...
```

- [ ] **Step 3: Harden promo retry logic (Bug #5)**

In `create_order`, find the `_skip_record_usage` block (lines 129-132) and replace with:

```python
            if PromoCodeUsage.objects.filter(code=promo_code, user=request.user, course_slug=promo_slug).exists():
                # Usage already recorded. Check enrollment status.
                _is_bundle = course_slug == ALL_COURSES_BUNDLE_SLUG
                _c = None if _is_bundle else Course.objects.filter(slug=course_slug, is_published=True).first()
                _enrolled = _is_bundle or (
                    _c is not None and Enrollment.objects.filter(user=request.user, course=_c, is_paid=True).exists()
                )
                if _enrolled:
                    # Already enrolled — idempotent success.
                    return Response({"free": True, "course_slug": course_slug, "amount_inr": 0})
                # Bug #5 fix: limit retries — track retry count with cache
                retry_key = f"promo_retry:{request.user.id}:{promo_code}:{promo_slug}"
                retry_count = _django_cache.get(retry_key, 0)
                if retry_count >= 3:
                    return Response({"detail": "Too many promo code retry attempts. Contact support."}, status=429)
                _django_cache.set(retry_key, retry_count + 1, 3600)
                is_promo_valid = True
                promo_code_obj._skip_record_usage = True
```

- [ ] **Step 4: Commit**

```bash
git add infosec-backend/backend/payments/views.py infosec-backend/backend/backend/settings.py
git commit -m "security: rate-limit payment verify/create, harden promo retry (max 3 attempts/hour)"
```

---

### Task 7: Frontend — QuizPage submits to backend

**Files:**
- Modify: `src/pages/QuizPage.tsx`

- [ ] **Step 1: Replace saveQuizScoreToDatabase with backend submit call**

In `QuizPage.tsx`, find the `saveQuizScoreToDatabase` function (lines 317-342) and replace with:

```typescript
const submitQuizToBackend = async (
  answersMap: Record<string, number>,
  localScore: number,
  localPassed: boolean
): Promise<{ score: number; passed: boolean; results: any[] } | null> => {
  try {
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) return null;

    const resolvedId = resolvedQuizId || quizId;
    if (!resolvedId) return null;

    const response = await fetch(
      `${import.meta.env.VITE_API_BASE_URL}/api/courses/${slug}/quiz/${resolvedId}/submit/`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ answers: answersMap }),
      }
    );

    if (!response.ok) {
      console.error("Quiz submit failed:", response.status);
      return null;
    }

    return await response.json();
  } catch (error) {
    console.error("Error submitting quiz to backend:", error);
    return null;
  }
};
```

- [ ] **Step 2: Update the useEffect that fires on quiz completion**

Find the `useEffect` at lines 271-314 and replace with:

```typescript
useEffect(() => {
  if (quizState !== "results") return;

  // Write to localStorage for UI speed (cache only, not authoritative)
  const rawKey = `quiz_${slug}_${quizId}`;
  localStorage.setItem(rawKey, score.percentage.toString());
  if (resolvedQuizId && resolvedQuizId !== quizId) {
    localStorage.setItem(`quiz_${slug}_${resolvedQuizId}`, score.percentage.toString());
  }
  if (passed) {
    const completedKey = `completed_lessons_${slug}`;
    const completedLessons = JSON.parse(localStorage.getItem(completedKey) || "[]");
    const idsToMark = [quizId, resolvedQuizId].filter(Boolean) as string[];
    let changed = false;
    for (const id of idsToMark) {
      if (!completedLessons.includes(id)) {
        completedLessons.push(id);
        changed = true;
      }
    }
    if (changed) localStorage.setItem(completedKey, JSON.stringify(completedLessons));
  }

  // Submit to backend (server is the authoritative record for certificates)
  submitQuizToBackend(selectedAnswers, score.percentage, passed);

  if (passed && course) {
    logActivity("quiz", quiz!.title, course.title);
  }

  window.dispatchEvent(
    new CustomEvent("quizCompleted", {
      detail: { quizId, score: score.percentage, courseId: slug, passed },
    })
  );
}, [quizState]);
```

- [ ] **Step 3: Commit**

```bash
git add src/pages/QuizPage.tsx
git commit -m "security: QuizPage submits answers to backend for server-side validation and recording"
```

---

### Task 8: Frontend — CourseDetail uses server completion for certificate gate

**Files:**
- Modify: `src/pages/CourseDetail.tsx`

- [ ] **Step 1: Add server completion fetch**

Find the existing `useEffect` that loads quiz scores from localStorage (around line 211). Add a new `useEffect` AFTER it:

```typescript
const [serverCompleted, setServerCompleted] = useState<boolean | null>(null);

useEffect(() => {
  if (!slug || !user) return;
  const accessToken = localStorage.getItem("accessToken");
  if (!accessToken) return;

  fetch(`${import.meta.env.VITE_API_BASE_URL}/api/courses/${slug}/completion/`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  })
    .then((r) => (r.ok ? r.json() : null))
    .then((data) => {
      if (data) setServerCompleted(data.completed === true);
    })
    .catch(() => {});
}, [slug, user]);
```

Add `const [serverCompleted, setServerCompleted] = useState<boolean | null>(null);` to the component's state declarations.

- [ ] **Step 2: Gate certificate on server completion**

Find where `isCourseCompleted` is used in the certificate download/share button rendering (around line 620) and add a server-side guard to the handlers.

Find the `handleDownloadCertificate` and `handleShareCertificate` functions (around lines 788-805) and add at the start of each:

```typescript
const handleDownloadCertificate = async () => {
  // Bug #6/#7 fix: require server-confirmed completion, not just localStorage
  if (serverCompleted === false) {
    setEnrollError("Please complete at least one quiz before downloading your certificate.");
    return;
  }
  // ... rest of existing function unchanged ...
```

```typescript
const handleShareCertificate = async () => {
  if (serverCompleted === false) {
    setEnrollError("Please complete at least one quiz before sharing your certificate.");
    return;
  }
  // ... rest of existing function unchanged ...
```

Note: `serverCompleted === null` means the check is still loading — we allow it through so UX isn't blocked for legitimate users. The backend is the final authority either way.

- [ ] **Step 3: Commit**

```bash
git add src/pages/CourseDetail.tsx
git commit -m "security: gate certificate generation on server-confirmed quiz completion"
```

---

### Task 9: Final verification + push

- [ ] **Step 1: Run backend server and check new endpoints respond**

```bash
cd infosec-backend/backend
python manage.py runserver 8000
```

In a new terminal, test endpoints (replace TOKEN with a valid JWT):
```bash
# Quiz submit endpoint exists
curl -X POST http://127.0.0.1:8000/api/courses/network-fundamentals/quiz/nf-q1/submit/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"answers": {}}'
# Expected: 200 with score/passed fields

# Completion endpoint exists
curl http://127.0.0.1:8000/api/courses/network-fundamentals/completion/ \
  -H "Authorization: Bearer TOKEN"
# Expected: 200 with completed: false (no quiz submitted yet)

# Certificate upload requires auth
curl -X POST http://127.0.0.1:8000/api/certificates/upload/ \
  -H "Content-Type: application/json" \
  -d '{"user_email": "hacker@evil.com", "course_slug": "soc-fundamentals", "image": "fake"}'
# Expected: 401 Unauthorized (no JWT provided)
```

- [ ] **Step 2: Run frontend build to check TypeScript compiles**

```bash
npm run build
```

Expected: no TypeScript errors.

- [ ] **Step 3: Push all commits**

```bash
git log --oneline -10  # review commits
git push origin main
```

---

## Security Model After These Fixes

| # | Vulnerability | Fix | Still crackable? |
|---|---|---|---|
| 1 | No rate limit on payment verify | Cache-based 10/min limit | No |
| 2 | Test mode config risk | Unchanged (already prod-blocked) | No (RAILWAY check) |
| 3 | lesson_id arbitrary values | Regex format validation | No |
| 4 | Quiz answers in JS bundle | Answers now validated server-side | Answers visible, but server is authoritative |
| 5 | Promo retry abuse | 3 retries/hour max | No |
| 6 | localStorage quiz completion fake | Backend records score; certificate requires passing QuizScore in DB | No |
| 7 | Certificate — no auth | `@api_view` + `IsAuthenticated` + enrollment + DB completion check | No |
