/**
 * usePageContext — derive the current page context from the active route so the
 * floating AI assistant can attach it to every message it sends.
 */

import { useLocation, useParams } from "react-router-dom";
import { useMemo } from "react";
import {
  buildPageContext,
  getCourseTitle,
  getLessonTitle,
  type PageContextPayload,
} from "@/lib/pageContext";

const PAGE_TITLES: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/labs": "Practice Labs",
  "/labs/alerts": "Alerts Lab",
  "/labs/incidents": "Incidents Lab",
  "/labs/endpoints": "Endpoints Lab",
  "/labs/threat-intel": "Threat Intelligence Lab",
  "/labs/email-security": "Email Security Lab",
  "/labs/settings": "Lab Settings",
  "/labs/logs": "Lab Logs",
  "/courses": "Course Catalog",
  "/chat": "AI Workspace",
};

export function usePageContext(): PageContextPayload {
  const location = useLocation();
  const params = useParams();
  const { slug, lessonId, courseId, resourceId, alertId } = params;

  return useMemo(() => {
    const { pathname } = location;

    if (slug && lessonId) {
      const courseTitle = getCourseTitle(slug);
      const lessonTitle = getLessonTitle(slug, lessonId);
      return buildPageContext({
        type: "lesson",
        course: slug,
        course_title: courseTitle,
        lesson: lessonId,
        lesson_title: lessonTitle,
      });
    }

    if (slug && params.quizId) {
      return buildPageContext({
        type: "quiz",
        course: slug,
        course_title: getCourseTitle(slug),
      });
    }

    if (slug && resourceId) {
      return buildPageContext({
        type: "lesson",
        course: slug,
        course_title: getCourseTitle(slug),
      });
    }

    if (slug) {
      return buildPageContext({
        type: "course",
        course: slug,
        course_title: getCourseTitle(slug),
      });
    }

    if (courseId && alertId) {
      return buildPageContext({
        type: "wazuh",
        lab: courseId,
        lab_title: PAGE_TITLES[`/labs/${courseId}`] || courseId,
        alert_id: alertId,
      });
    }

    if (pathname === "/dashboard") return buildPageContext({ type: "dashboard" });
    if (pathname === "/labs") return buildPageContext({ type: "lab", lab_title: "Practice Labs" });
    if (pathname === "/labs/settings") return buildPageContext({ type: "settings" });
    if (pathname === "/labs/logs") return buildPageContext({ type: "logs" });
    if (pathname === "/labs/threat-intel") return buildPageContext({ type: "threat_intel", lab_title: "Threat Intelligence Lab" });
    if (pathname === "/labs/email-security") return buildPageContext({ type: "email_security", lab_title: "Email Security Lab" });
    if (pathname === "/labs/alerts") return buildPageContext({ type: "alerts", lab_title: "Alerts Lab" });
    if (pathname === "/labs/incidents") return buildPageContext({ type: "incidents", lab_title: "Incidents Lab" });
    if (pathname === "/labs/endpoints") return buildPageContext({ type: "endpoints", lab_title: "Endpoints Lab" });
    if (pathname.startsWith("/courses")) return buildPageContext({ type: "course" });
    if (pathname.startsWith("/chat")) return buildPageContext({ type: "workspace" });

    return buildPageContext({ type: "page" });
  }, [location, slug, lessonId, courseId, resourceId, alertId, params.quizId]);
}
