/**
 * export_lesson_content.ts
 * ────────────────────────
 * Exports every lesson from the TypeScript data files into a single JSON file
 * that the Django management command `import_lesson_content` can read.
 *
 * Run:
 *   npx tsx scripts/export_lesson_content.ts
 *
 * Output:
 *   infosec-backend/backend/courses/lesson_data/all_lessons.json
 *
 * Priority rule (mirrors LessonViewer.tsx):
 *   lessonContent.ts (main) > lessons/*.ts (per-course)
 *   When both sources have the same (courseId, lessonId), the main file wins.
 */

import { writeFileSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

// ── Data imports ──────────────────────────────────────────────────────────────
// Use the public API from index.ts — it already handles all per-course imports.
import {
  getLessonContentFromPerCourse,
  getCourseLessonsFromPerCourse,
} from "../src/data/lessons/index";

// Main lessonContent.ts — has higher priority than per-course files.
import { lessonContents as mainLessons } from "../src/data/lessonContent";

// ── Course ID ↔ URL slug mapping ─────────────────────────────────────────────
// Internal courseId (used in lesson TS files) → URL slug (used in Django API).
// This is the *reverse* of the normalizeCourseId map in lessons/index.ts and
// the lessonsCourseId map in LessonViewer.tsx.
const COURSE_ID_TO_SLUG: Record<string, string> = {
  "soc-fundamentals":           "blue-team-soc-fundamentals",
  "log-analysis":               "log-analysis-for-beginners",
  "network-fundamentals":       "network-fundamentals",
  "siem-fundamentals":          "siem-fundamentals",
  "incident-response":          "incident-response-fundamentals",
  "soc-analyst-path":           "soc-analyst-path",
  "network-security-monitoring": "network-security-monitoring",
  "detection-engineering":      "detection-engineering-basics",
  "malware-analysis":           "malware-analysis-fundamentals",
  "threat-hunting":             "threat-hunting-fundamentals",
  // Draft / unlaunched courses kept in the DB so admins can preview.
  "cybersecurity-frameworks":   "cybersecurity-frameworks",
  "soc-analyst-practical":      "soc-analyst-practical-training",
};

// All internal courseIds present in lessons/index.ts.
const ALL_INTERNAL_COURSE_IDS = Object.keys(COURSE_ID_TO_SLUG);

// ── Build merged lesson map ───────────────────────────────────────────────────
// Key: URL slug   Value: { lessonId → lessonData }
const bySlug: Record<string, Record<string, Record<string, unknown>>> = {};

function ensureSlug(slug: string) {
  if (!bySlug[slug]) bySlug[slug] = {};
}

// Pass 1: per-course files (lower priority — will be overwritten by main)
for (const courseId of ALL_INTERNAL_COURSE_IDS) {
  const lessons = getCourseLessonsFromPerCourse(courseId);
  if (!lessons || lessons.length === 0) continue;

  const slug = COURSE_ID_TO_SLUG[courseId] ?? courseId;
  ensureSlug(slug);

  for (const lesson of lessons) {
    const id = (lesson as any).id as string;
    if (!id) continue;
    bySlug[slug][id] = lesson as Record<string, unknown>;
  }
}

// Pass 2: main lessonContent.ts (higher priority — overwrites per-course)
for (const lesson of mainLessons) {
  const courseId = (lesson as any).courseId as string;
  if (!courseId) continue;

  const slug = COURSE_ID_TO_SLUG[courseId] ?? courseId;
  ensureSlug(slug);

  const id = (lesson as any).id as string;
  if (!id) continue;

  bySlug[slug][id] = lesson as Record<string, unknown>;
}

// ── Convert to output format ──────────────────────────────────────────────────
// { slug: [ lesson, ... ] }  — sorted by lesson ID for deterministic diffs.
const output: Record<string, unknown[]> = {};

for (const [slug, lessonMap] of Object.entries(bySlug)) {
  if (Object.keys(lessonMap).length === 0) continue;

  // Sort by lesson ID so git diffs are stable.
  output[slug] = Object.entries(lessonMap)
    .sort(([a], [b]) => a.localeCompare(b, undefined, { numeric: true }))
    .map(([, lesson]) => lesson);
}

// ── Write JSON ────────────────────────────────────────────────────────────────
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const outDir = join(
  __dirname,
  "..",
  "infosec-backend",
  "backend",
  "courses",
  "lesson_data",
);
mkdirSync(outDir, { recursive: true });

const outPath = join(outDir, "all_lessons.json");
writeFileSync(outPath, JSON.stringify(output, null, 2), "utf-8");

// ── Summary ───────────────────────────────────────────────────────────────────
console.log(`\n✅  Lesson content exported → ${outPath}\n`);
let total = 0;
for (const [slug, lessons] of Object.entries(output)) {
  console.log(`   ${slug.padEnd(40)} ${(lessons as unknown[]).length} lessons`);
  total += (lessons as unknown[]).length;
}
console.log(`\n   Total: ${total} lessons across ${Object.keys(output).length} courses\n`);
