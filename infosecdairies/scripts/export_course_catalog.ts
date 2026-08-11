/**
 * Export the frontend course catalog (metadata only) as JSON.
 *
 * Produces a file consumed by the AI service knowledge ingestion pipeline:
 *   ai_service/app/knowledge/data/course_catalog.json
 *
 * The catalog is keyed by the lesson-content slug used in
 * infosec-backend/backend/courses/lesson_data/all_lessons.json.
 *
 * Run:
 *   node node_modules/esbuild/bin/esbuild --bundle scripts/export_course_catalog.ts \
 *     --format=cjs --platform=node --alias:@=./src \
 *     --outfile=scripts/.catalog.cjs && node scripts/.catalog.cjs
 */
import { courses } from "../src/data/courses";
import { writeFileSync, mkdirSync } from "fs";
import { dirname, join, resolve } from "path";

// Frontend course id -> lesson-content slug (all_lessons.json)
const ID_TO_SLUG: Record<string, string> = {
  "soc-fundamentals": "blue-team-soc-fundamentals",
  "log-analysis": "log-analysis-for-beginners",
  "network-fundamentals": "network-fundamentals",
  "siem-fundamentals": "siem-fundamentals",
  "incident-response": "incident-response-fundamentals",
  "soc-analyst-path": "soc-analyst-path",
  "network-security-monitoring": "network-security-monitoring",
  "detection-engineering": "detection-engineering-basics",
  "malware-analysis": "malware-analysis-fundamentals",
  "threat-hunting": "threat-hunting-fundamentals",
  "cybersecurity-frameworks": "cybersecurity-frameworks",
};

const catalog: Record<string, any> = {};

for (const course of courses) {
  const slug = ID_TO_SLUG[course.id] || course.id;
  catalog[slug] = {
    id: course.id,
    slug,
    title: course.title,
    shortTitle: course.shortTitle,
    description: course.description,
    difficulty: course.difficulty,
    duration: course.duration,
    modules: (course.modules || []).map((m) => ({
      id: m.id,
      title: m.title,
      lessons: (m.lessons || []).map((l) => ({
        id: l.id,
        title: l.title,
        description: l.description || "",
      })),
    })),
  };
}

const outPath = resolve(
  __dirname,
  "../../ai_service/app/knowledge/data/course_catalog.json",
);
mkdirSync(dirname(outPath), { recursive: true });
writeFileSync(outPath, JSON.stringify(catalog, null, 2));
console.log(
  `Wrote course catalog for ${Object.keys(catalog).length} courses -> ${outPath}`,
);
