import { LessonContent } from "../lessonContent";
import { lessonContents as socLessons } from "./socFundamentals";
import { lessonContents as logLessons } from "./logAnalysisForBeginners";
import { lessonContents as networkFundamentalsLessons } from "./networkFundamentals";
import { lessonContents as siemFundamentalsLessons } from "./siemFundamentals";
import { lessonContents as incidentResponseLessons } from "./incidentResponse";
import { socAnalystLearningPath } from "./socAnalystLearningPath";
import { networkSecurityMonitoring } from "./networkSecurityMonitoring";
import { detectionEngineeringBasics } from "./detectionEngineeringBasics";
import { malwareAnalysisFundamentals } from "./malwareAnalysisFundamentals";
import { threatHuntingFundamentals } from "./threatHuntingFundamentals";

const lessonsByCourse: Record<string, LessonContent[]> = {
  "soc-fundamentals": socLessons,
  "log-analysis": logLessons,
  "network-fundamentals": networkFundamentalsLessons,
  "siem-fundamentals": siemFundamentalsLessons,
  "incident-response": incidentResponseLessons,
  "soc-analyst-path": socAnalystLearningPath,
  "network-security-monitoring": networkSecurityMonitoring,
  "detection-engineering": detectionEngineeringBasics,
  "malware-analysis": malwareAnalysisFundamentals,
  "threat-hunting": threatHuntingFundamentals,
};

const normalizeCourseId = (courseId: string): string => {
  switch (courseId) {
    case "blue-team-soc-fundamentals":
      return "soc-fundamentals";
    case "log-analysis-for-beginners":
      return "log-analysis";
    case "siem-fundamentals":
      return "siem-fundamentals";
    case "incident-response":
      return "incident-response";
    case "network-fundamentals":
      return "network-fundamentals";
    case "soc-analyst-path":
      return "soc-analyst-path";
    case "network-security-monitoring":
      return "network-security-monitoring";
    case "detection-engineering-basics":
      return "detection-engineering";
    case "malware-analysis-fundamentals":
      return "malware-analysis";
    case "threat-hunting-fundamentals":
      return "threat-hunting";
    default:
      return courseId;
  }
};

export const getLessonContentFromPerCourse = (
  courseId: string,
  lessonId: string,
): LessonContent | undefined => {
  const normalized = normalizeCourseId(courseId);
  const list = lessonsByCourse[normalized];
  if (!list) return undefined;
  return list.find((lesson) => lesson.id === lessonId);
};

export const getCourseLessonsFromPerCourse = (
  courseId: string,
): LessonContent[] | undefined => {
  const normalized = normalizeCourseId(courseId);
  return lessonsByCourse[normalized];
};
