# Platform API Inventory

This document maps out the available endpoints from the BlueTeamers Django backend (`infosec-backend`), highlighting what is currently available for integration and identifying gaps according to the Phase 8 requirements.

## 1. Authentication & User Profile (`/api/auth/`)

**Available Endpoints:**
- `POST /api/auth/register/`: User registration.
- `POST /api/auth/login/`: Basic JWT login. Returns access and refresh tokens.
- `POST /api/auth/verify/`: Verifies JWT tokens.
- `POST /api/auth/token/refresh/`: Refreshes expired JWT tokens.
- `POST /api/auth/verify-email/`: OTP based email verification.
- `POST /api/auth/resend-verification-otp/`: Resends OTP.
- `POST /api/auth/password-reset/request/`: Initiates password reset.
- `POST /api/auth/password-reset/confirm/`: Completes password reset.
- `POST /api/auth/google/jwt/`: Google SSO login.
- `POST /api/auth/profile/`: Updates or retrieves user profile metadata.

## 2. Courses & Progress (`/api/courses/`)

**Available Endpoints:**
- `GET /api/courses/`: Lists all available courses (The Course Catalog).
- `GET /api/courses/<slug>/`: Detailed view of a specific course, including its modules and lessons.
- `POST /api/courses/<slug>/enroll/`: Enrolls the authenticated user in a course.
- `GET /api/courses/<slug>/enrollment/`: Checks the enrollment status for the user.
- `GET /api/courses/<slug>/access-token/`: Grants an access token for course media/labs.
- `GET /api/courses/<slug>/progress/`: Returns the completion progress of the course.
- `GET /api/courses/<slug>/completion/`: Retrieves course completion status or triggers graduation logic.
- `GET /api/courses/<slug>/lessons/<lesson_id>/content/`: Retrieves the specific content/markdown of a lesson.
- `POST /api/courses/<slug>/lessons/<lesson_id>/complete/`: Marks a lesson as complete for the user.

## 3. Assessments & Labs (`/api/courses/`)

**Available Endpoints:**
- `GET /api/courses/<slug>/quiz-scores/`: Retrieves the user's past quiz scores.
- `POST /api/courses/<slug>/quiz/<quiz_id>/submit/`: Submits answers for a quiz (Assessment) and returns the grade.
- `POST /api/courses/<slug>/lessons/<lesson_id>/lab-questions/<question_id>/submit/`: Submits flags/answers for interactive lab components.

## 4. Certificates (`/api/certificates/`)

**Available Endpoints:**
- `POST /api/certificates/upload/`: Uploads a generated certificate.
- `POST /api/certificates/share/`: Generates sharing links/metadata.
- `GET /api/certificates/lookup/<cert_id>/`: Public verification endpoint for a certificate.
- `GET /api/certificates/my/<slug>/`: Retrieves the certificate for a specific completed course.

## 5. Payments (`/api/payments/`)

**Available Endpoints:**
- `POST /api/payments/create-order/`: Creates a Razorpay order.
- `POST /api/payments/verify/`: Verifies payment signature.
- `GET /api/payments/my-purchases/`: Lists user's purchases.
- `GET /api/payments/pricing/`: Retrieves pricing data.

## 6. Identified Gaps (Missing APIs)

The following entities requested in Phase 8 do not currently exist in the Django backend routing:
- **Learning Paths:** No `/api/learning-paths/` endpoints.
- **Badges:** No `/api/badges/` endpoints for gamification.
- **Dashboard:** No consolidated `/api/dashboard/` endpoint (the frontend currently aggregates courses + progress).
- **Recommendations:** No `/api/recommendations/` endpoints (this will be built inside the `PlatformExecutionEngine` / AI Service as per Phase 8).

*Note: For the entities that do not exist in Django, we will either need to create mock adapters in our `PlatformRepository` (until the Django backend supports them) or temporarily omit them from the RAG context.*
