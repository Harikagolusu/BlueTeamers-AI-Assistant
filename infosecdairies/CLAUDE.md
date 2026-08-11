# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```sh
npm run dev        # Start dev server on port 8081
npm run build      # Production build
npm run build:dev  # Dev-mode build
npm run lint       # ESLint
npm run preview    # Preview production build
```

No test runner is configured — there are no test files in this project.

### Backend (Django)

```sh
cd infosec-backend/backend
bash setup_dev.sh                 # First-time setup: migrate + seed courses
python manage.py runserver        # Start Django on port 8000
python manage.py migrate          # Apply migrations
python manage.py makemigrations   # Create new migrations
```

## Architecture

This is a cybersecurity e-learning platform (InfoSec Dairies) built with React + Vite. It has two parts:

### Frontend (`src/`)

**Stack:** React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui (Radix), React Router v6, TanStack Query, Recharts, React Hook Form + Zod

**Path alias:** `@/` maps to `src/`

**Routing** is defined in `src/App.tsx`. Key routes:
- `/` — landing page composed of section components
- `/courses/:slug` — course detail with modules, quizzes, resources
- `/courses/:slug/lesson/:lessonId` — lesson viewer
- `/courses/:slug/quiz/:quizId` — quiz player
- `/courses/:slug/checkout` — payment/enrollment
- `/dashboard` — authenticated user dashboard
- `/verify/:slug/:emailHash` — certificate verification
- `/live-courses/:courseId` — live cohort course detail

**Auth** (`src/context/AuthContext.tsx`): JWT-based, tokens stored in `localStorage` (`accessToken`, `refreshToken`, `userEmail`, `userFullName`). Auto-refreshes every 10 minutes. `useAuth()` hook provides `{ user, isAuthenticated, login, logout }`.

**API** (`src/services/api.ts`): All requests go to `VITE_API_BASE_URL` (defaults to `http://127.0.0.1:8000`). In dev without `VITE_API_BASE_URL`, `/api/*` requests use the Vite proxy to `localhost:8000`.

**Course data** lives in two places:
- `src/data/courses.ts` — static course metadata (modules, quizzes, resources), exported as `courses` array
- `src/data/lessons/` — lesson content per course, keyed by course slug via `getLessonContentFromPerCourse()` in `src/data/lessons/index.ts`
- `src/data/quizData.ts` — quiz questions, answers, explanations
- `src/data/liveCourses.ts` — live cohort course data (separate from self-paced courses)
- Course slugs in data files sometimes differ from URL slugs; `normalizeCourseId()` in `src/data/lessons/index.ts` handles the mapping

**Pricing:** `FREE_COURSE_SLUG = "network-fundamentals"`, `ALL_COURSES_BUNDLE_SLUG = "all-courses-bundle"` (₹3,999). Per-difficulty pricing: easy ₹499, medium ₹799, hard ₹1,199.

**UI components** (`src/components/ui/`) are shadcn/ui primitives — edit with caution or regenerate via shadcn CLI.

### Backend (`infosec-backend/backend/`)

**Stack:** Django 6, Django REST Framework, dj-rest-auth, django-allauth (Google + LinkedIn OAuth), Simple JWT

**Apps:** `accounts`, `courses`, `certificates`, `payments`, `leads`

**API prefix:** all endpoints are under `/api/` (e.g. `/api/auth/`, `/api/courses/`, `/api/certificates/`, `/api/payments/`, `/api/leads/`)

Auth uses JWT (access + refresh tokens). Token refresh endpoint: `/api/auth/token/refresh/`.

Config via `python-decouple` — requires `.env` at `infosec-backend/backend/.env`.
