/**
 * lessonContent.ts — type definitions only.
 *
 * The actual lesson content has been moved server-side and is served by the
 * Django backend at:
 *   GET /api/courses/{slug}/lessons/{lesson_id}/content/
 *
 * Access requires a valid auth JWT + an enrolled, paid account for the course.
 * This prevents bundle-extraction attacks (downloading the Vite JS bundle and
 * reading every lesson without paying).
 *
 * To regenerate the DB from the source-of-truth JSON:
 *   npx tsx scripts/export_lesson_content.ts
 *   python manage.py import_lesson_content
 */

export interface LabQuestion {
  id: string;
  question: string;
  /** Not present in GET response — returned by the submit endpoint only when correct or attempts exhausted. */
  answer?: string;
  hint?: string;
}

export interface LessonContent {
  id: string;
  courseId: string;
  title: string;
  content: string;
  quiz?: string;
  keyTakeaways?: string[];
  practicalExercise?: {
    title: string;
    description: string;
    steps: string[];
    labScenario?: string;
    labQuestions?: LabQuestion[];
  };
  additionalResources?: {
    title: string;
    url?: string;
    type: "video" | "article" | "tool" | "documentation";
  }[];
}

// Content has been moved to the Django backend.
// These stubs keep existing imports from breaking while contributing zero bytes
// of lesson text to the browser JS bundle.
export const lessonContents: LessonContent[] = [];

export const getLessonContent = (
  _courseId: string,
  _lessonId: string,
): LessonContent | undefined => undefined;

export const getCourseLessons = (_courseId: string): LessonContent[] => [];
