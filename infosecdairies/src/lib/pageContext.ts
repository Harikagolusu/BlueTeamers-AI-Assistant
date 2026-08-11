/**
 * pageContext.ts — automatic page-context detection for the floating AI assistant.
 *
 * The assistant detects where the learner currently is (Dashboard, Course, Lesson,
 * Practice Lab, Wazuh Lab, ...) and sends a structured `context.page` payload with
 * each chat message. The AI backend's PageContextStage reads it and injects a
 * "[Page Context]" block into the system prompt, so the AI already knows which
 * lesson or lab is open without the user having to explain.
 */

import { getCourseById } from "@/data/courses";
import { getLessonContentFromPerCourse } from "@/data/lessons";

export interface PageContextPayload {
  type: string;
  path: string;
  course?: string;
  course_title?: string;
  lesson?: string;
  lesson_title?: string;
  lab?: string;
  lab_title?: string;
  alert_id?: string;
}

const COURSE_SLUG_TO_DATA_ID: Record<string, string> = {
  "blue-team-soc-fundamentals": "soc-fundamentals",
  "log-analysis-for-beginners": "log-analysis",
  "soc-analyst-practical-training": "soc-analyst-path",
  "incident-response-fundamentals": "incident-response",
  "network-fundamentals": "network-fundamentals",
  "siem-fundamentals": "siem-fundamentals",
  "soc-analyst-path": "soc-analyst-path",
  "network-security-monitoring": "network-security-monitoring",
  "detection-engineering-basics": "detection-engineering",
  "malware-analysis-fundamentals": "malware-analysis",
  "threat-hunting-fundamentals": "threat-hunting",
};

export function resolveCourseDataId(slug: string): string {
  return COURSE_SLUG_TO_DATA_ID[slug] || slug;
}

export function getCourseTitle(slug?: string): string | undefined {
  if (!slug) return undefined;
  return getCourseById(resolveCourseDataId(slug))?.title;
}

export function getLessonTitle(courseSlug?: string, lessonId?: string): string | undefined {
  if (!courseSlug || !lessonId) return undefined;
  return getLessonContentFromPerCourse(resolveCourseDataId(courseSlug), lessonId)?.title;
}

export function buildPageContext(payload: Partial<PageContextPayload>): PageContextPayload {
  const page: PageContextPayload = {
    type: payload.type || "page",
    path: payload.path || window.location.pathname,
  };
  if (payload.course) page.course = payload.course;
  if (payload.course_title) page.course_title = payload.course_title;
  if (payload.lesson) page.lesson = payload.lesson;
  if (payload.lesson_title) page.lesson_title = payload.lesson_title;
  if (payload.lab) page.lab = payload.lab;
  if (payload.lab_title) page.lab_title = payload.lab_title;
  if (payload.alert_id) page.alert_id = payload.alert_id;
  return page;
}
