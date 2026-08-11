import { useState, useEffect, useMemo, useCallback } from "react";
import { Link, useParams, Navigate, useNavigate, useLocation } from "react-router-dom";
import Navbar from "@/components/Navbar";
import {
  Shield, ChevronLeft, ChevronRight, CheckCircle, Clock, BookOpen,
  Lightbulb, FlaskConical, ExternalLink, Menu, X, Lock, FileQuestion,
  HelpCircle, Eye, EyeOff, Send
} from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { getCourseById, Course, Lesson, Module } from "@/data/courses";
import type { LessonContent, LabQuestion } from "@/data/lessonContent";
import { ScrollArea } from "@/components/ui/scroll-area";
import { apiUrl } from "@/services/api";
import { logActivity } from "./Dashboard";
import { useCourseAccess } from "@/hooks/useCourseAccess";
import { useLessonContent } from "@/hooks/useLessonContent";
import { TESTING_MODE } from "@/lib/testingMode";

// Import course backgrounds
import socFundamentalsBg from "@/assets/soc-course-bg.jpg";
import logAnalysisBg from "@/assets/courses/log-analysis-bg.jpg";
import siemFundamentalsBg from "@/assets/courses/siem-fundamentals-bg.jpg";
import socAnalystPracticalBg from "@/assets/courses/soc-analyst-practical-bg.jpg";
import incidentResponseBg from "@/assets/courses/incident-response-bg.jpg";
import threatHuntingBg from "@/assets/courses/threat-hunting-bg.jpg";
import detectionEngineeringBg from "@/assets/courses/detection-engineering-bg.jpg";
import malwareAnalysisBg from "@/assets/courses/malware-analysis-bg.jpg";
import networkFundamentalsBg from "@/assets/courses/network-fundamentals-bg.jpg";

const courseBackgrounds: Record<string, string> = {
  "blue-team-soc-fundamentals": socFundamentalsBg,
  "log-analysis": logAnalysisBg,
  "siem-fundamentals": siemFundamentalsBg,
  "soc-analyst-practical": socAnalystPracticalBg,
  "incident-response": incidentResponseBg,
  "threat-hunting": threatHuntingBg,
  "detection-engineering": detectionEngineeringBg,
  "malware-analysis": malwareAnalysisBg,
  "network-fundamentals": networkFundamentalsBg,
};

interface LabSubmitResult {
  correct: boolean;
  attempts: number;
  reference_answer: string | null;
}

const LabQuestionsSection = ({
  scenario,
  questions,
  slug,
  lessonId,
}: {
  scenario?: string;
  questions: LabQuestion[];
  slug: string;
  lessonId: string;
}) => {
  const [userAnswers, setUserAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState<Record<string, boolean>>({});
  const [showHint, setShowHint] = useState<Record<string, boolean>>({});
  const [showAnswer, setShowAnswer] = useState<Record<string, boolean>>({});
  const [results, setResults] = useState<Record<string, LabSubmitResult>>({});
  const [submitting, setSubmitting] = useState<Record<string, boolean>>({});

  const isLocked = (qId: string) => {
    const r = results[qId];
    return submitted[qId] && !!r && (r.correct || r.attempts >= 4);
  };

  const handleSubmit = async (qId: string) => {
    const answer = (userAnswers[qId] || "").trim();
    if (!answer || submitting[qId]) return;
    setSubmitting(prev => ({ ...prev, [qId]: true }));
    try {
      const authToken = localStorage.getItem("accessToken");
      const res = await fetch(
        apiUrl(`/api/courses/${slug}/lessons/${lessonId}/lab-questions/${qId}/submit/`),
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
          },
          body: JSON.stringify({ answer }),
        }
      );
      if (res.ok) {
        const data: LabSubmitResult = await res.json();
        setResults(prev => ({ ...prev, [qId]: data }));
        setSubmitted(prev => ({ ...prev, [qId]: true }));
      }
    } catch {
      // network error — leave input intact so the user can retry
    } finally {
      setSubmitting(prev => ({ ...prev, [qId]: false }));
    }
  };

  const handleRetry = (qId: string) => {
    setUserAnswers(prev => ({ ...prev, [qId]: "" }));
    setSubmitted(prev => ({ ...prev, [qId]: false }));
  };

  return (
    <div className="mt-6 space-y-4">
      <div className="flex items-center gap-2 mb-2">
        <HelpCircle className="w-4 h-4 text-cyan-400" />
        <h4 className="text-sm font-semibold text-cyan-400 uppercase tracking-wider">Scenario Lab</h4>
      </div>

      {scenario && (
        <div className="p-4 rounded-lg bg-cyan-500/5 border border-cyan-500/20 space-y-2">
          <p className="text-xs font-semibold text-cyan-400 uppercase tracking-wider">Scenario</p>
          <p className="text-sm text-muted-foreground leading-relaxed">{scenario}</p>
        </div>
      )}

      {questions.map((q, idx) => {
        const result = results[q.id];
        const locked = isLocked(q.id);
        const isSubmitted = submitted[q.id];
        const isSubmitting = submitting[q.id];
        const correct = result?.correct ?? false;
        const attemptsExhausted = (result?.attempts ?? 0) >= 4;

        return (
          <div key={q.id} className="p-4 rounded-lg bg-background/40 border border-white/[0.06] space-y-3">
            <div className="flex items-start gap-2">
              <span className="flex-shrink-0 w-5 h-5 rounded bg-cyan-500/20 text-cyan-400 text-xs flex items-center justify-center font-bold mt-0.5">
                {idx + 1}
              </span>
              <p className="text-sm font-medium text-foreground">{q.question}</p>
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Type your answer..."
                value={userAnswers[q.id] || ""}
                onChange={e => setUserAnswers(prev => ({ ...prev, [q.id]: e.target.value }))}
                onKeyDown={e => {
                  if (e.key === "Enter" && userAnswers[q.id]?.trim() && !locked && !isSubmitted)
                    handleSubmit(q.id);
                }}
                disabled={locked}
                className="flex-1 px-3 py-2 text-sm rounded-md bg-background/60 border border-white/[0.1] text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:border-cyan-500/50 disabled:opacity-60"
              />
              {!locked && !isSubmitted && (
                <button
                  onClick={() => handleSubmit(q.id)}
                  disabled={!userAnswers[q.id]?.trim() || isSubmitting}
                  className="px-3 py-2 rounded-md bg-cyan-600/80 text-white text-sm font-medium hover:bg-cyan-600 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 transition-colors"
                >
                  <Send className="w-3.5 h-3.5" />
                  {isSubmitting ? "..." : "Submit"}
                </button>
              )}
            </div>

            {q.hint && !locked && !isSubmitted && (
              <button
                onClick={() => setShowHint(prev => ({ ...prev, [q.id]: !prev[q.id] }))}
                className="text-xs text-yellow-500/80 hover:text-yellow-400 flex items-center gap-1 transition-colors"
              >
                <Lightbulb className="w-3 h-3" />
                {showHint[q.id] ? "Hide hint" : "Show hint"}
              </button>
            )}
            {showHint[q.id] && !locked && !isSubmitted && (
              <p className="text-xs text-yellow-500/70 pl-4 border-l-2 border-yellow-500/30">{q.hint}</p>
            )}

            {isSubmitted && (
              <div className="space-y-2">
                {correct ? (
                  <div className="flex items-center gap-2 text-sm font-medium text-emerald-400">
                    <CheckCircle className="w-4 h-4" /> Great answer!
                  </div>
                ) : (
                  <div className="space-y-2">
                    <div className="flex items-center gap-2 text-sm font-medium text-orange-400">
                      <Eye className="w-4 h-4" /> Incorrect {attemptsExhausted ? "— All attempts used." : ""}
                    </div>
                    {!attemptsExhausted && (
                      <button
                        onClick={() => handleRetry(q.id)}
                        className="text-xs text-cyan-400/80 hover:text-cyan-300 flex items-center gap-1 transition-colors"
                      >
                        Try again
                      </button>
                    )}
                  </div>
                )}

                {locked && attemptsExhausted && !correct && result?.reference_answer && (
                  <>
                    <button
                      onClick={() => setShowAnswer(prev => ({ ...prev, [q.id]: !prev[q.id] }))}
                      className="text-xs text-cyan-400/80 hover:text-cyan-300 flex items-center gap-1 transition-colors"
                    >
                      {showAnswer[q.id] ? <><EyeOff className="w-3 h-3" /> Hide answer</> : <><Eye className="w-3 h-3" /> Show answer</>}
                    </button>
                    {showAnswer[q.id] && (
                      <div className="p-3 rounded-md bg-emerald-500/10 border border-emerald-500/20">
                        <p className="text-sm text-emerald-300"><span className="font-semibold">Answer:</span> {result.reference_answer}</p>
                      </div>
                    )}
                  </>
                )}

                {correct && result?.reference_answer && (
                  <>
                    <button
                      onClick={() => setShowAnswer(prev => ({ ...prev, [q.id]: !prev[q.id] }))}
                      className="text-xs text-cyan-400/80 hover:text-cyan-300 flex items-center gap-1 transition-colors"
                    >
                      {showAnswer[q.id] ? <><EyeOff className="w-3 h-3" /> Hide answer</> : <><Eye className="w-3 h-3" /> View reference answer</>}
                    </button>
                    {showAnswer[q.id] && (
                      <div className="p-3 rounded-md bg-emerald-500/10 border border-emerald-500/20">
                        <p className="text-sm text-emerald-300"><span className="font-semibold">Answer:</span> {result.reference_answer}</p>
                      </div>
                    )}
                  </>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};

const LessonViewer = () => {
  const { slug, lessonId } = useParams<{ slug: string; lessonId: string }>();
  const navigate = useNavigate();
  const location = useLocation();

  // SECURITY: verify paid enrollment via RS256-signed token before rendering any content.
  // Layer 1: only RS256 accepted — HS256/none forgery attempts are rejected outright.
  // Layer 2: token user_id is bound to the current session — stolen tokens are rejected.
  // Layer 3: lesson content is fetched from the backend (never in the JS bundle).
  const { accessState, isStaff } = useCourseAccess(slug);

  // Fetch lesson content from the backend API.
  // Only fires once accessState === "granted" — no wasted 403s.
  const { lessonContent, contentLoading } = useLessonContent(slug, lessonId, accessState);

  const [sidebarOpen, setSidebarOpen] = useState(() => window.innerWidth >= 768);
  const [markingComplete, setMarkingComplete] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [completedLessonIds, setCompletedLessonIds] = useState<string[]>([]);
  const [progressLoaded, setProgressLoaded] = useState(false);

  const formatModuleId = (id: string) => id.replace(/^[a-z]+-/, "");

  const resolveQuizStorageId = (lessonLikeQuizId: string): string => {
    if (!slug) return lessonLikeQuizId;

    if (slug === "blue-team-soc-fundamentals") {
      const socQuizMap: Record<string, string> = {
        "1.5": "q1",
        "2.5": "q2",
        "3.6": "q3",
        "4.6": "q4",
        "5.6": "q4",
        "6.6": "q5",
        "7.6": "q6",
        "8.5": "q7",
        "9.5": "q8",
        "10.4": "q9",
      };
      return socQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
    }

    if (slug === "threat-hunting-fundamentals") {
      const thQuizMap: Record<string, string> = {
        "1.5": "th-q1",
        "2.5": "th-q2",
        "3.5": "th-q3",
        "4.5": "th-q4",
        "5.5": "th-q5",
        "6.5": "th-q6",
      };
      return thQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
    }

    if (slug === "network-security-monitoring") {
      const nsmQuizMap: Record<string, string> = {
        "1.5": "nsm-q1",
        "2.6": "nsm-q2",
        "3.5": "nsm-q3",
        "4.5": "nsm-q4",
        "5.5": "nsm-q5",
        "6.5": "nsm-q6",
      };
      return nsmQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
    }

    if (slug === "log-analysis-for-beginners") {
      const laQuizMap: Record<string, string> = {
        "1.5": "la-q1",
        "2.7": "la-q2",
        "3.6": "la-q3",
        "4.5": "la-q4",
        "5.5": "la-q5",
        "6.5": "la-q5",
      };
      return laQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
    }

    if (slug === "soc-analyst-path") {
      const sapQuizMap: Record<string, string> = {
        "1.7": "sap-q1",
        "2.7": "sap-q2",
        "3.7": "sap-q3",
        "4.7": "sap-q4",
        "5.7": "sap-q5",
        "6.7": "sap-q6",
        "7.7": "sap-q7",
        "8.7": "sap-q8",
        "9.7": "sap-q9",
        "10.7": "sap-q10",
        "11.7": "sap-q11",
        "12.7": "sap-q12",
      };
      return sapQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
    }

    if (slug === "detection-engineering-basics") {
      const deQuizMap: Record<string, string> = {
        "1.5": "de-q1",
        "2.5": "de-q2",
        "3.5": "de-q3",
        "4.5": "de-q4",
        "5.5": "de-q5",
        "6.5": "de-q6",
      };
      return deQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
    }

    if (slug === "malware-analysis-fundamentals") {
      const maQuizMap: Record<string, string> = {
        "1.5": "ma-q1",
        "2.5": "ma-q2",
        "3.5": "ma-q3",
        "4.5": "ma-q4",
        "5.5": "ma-q5",
        "6.5": "ma-q6",
      };
      return maQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
    }

    return lessonLikeQuizId;
  };

  // ─── FIX: Try multiple key formats so we always find the stored score ───
  // QuizPage saves under both raw ID (e.g. "6.5") and resolved ID (e.g. "q6").
  // We check both here so the gate never incorrectly thinks a quiz wasn't passed.
  const getStoredQuizScore = (lessonLikeQuizId: string): number | null => {
    if (!slug) return null;

    const resolved = resolveQuizStorageId(lessonLikeQuizId);

    // Build a deduplicated list of keys to try, most-specific first
    const keysToTry = Array.from(
      new Set([
        `quiz_${slug}_${resolved}`,          // e.g. quiz_blue-team-soc-fundamentals_q6
        `quiz_${slug}_${lessonLikeQuizId}`,  // e.g. quiz_blue-team-soc-fundamentals_6.5
      ])
    );

    for (const key of keysToTry) {
      const raw = localStorage.getItem(key);
      if (raw != null) {
        const score = Number(raw);
        if (!Number.isNaN(score)) return score;
      }
    }

    return null;
  };

  const getModuleGateQuizId = (module: any): string | null => {
    if (!module) return null;
    if (module.quizId) return String(module.quizId);
    return null;
  };

  const courseIdForMeta = useMemo(() => {
    if (!slug) return "";

    switch (slug) {
      case "blue-team-soc-fundamentals":
        return "soc-fundamentals";
      case "log-analysis-for-beginners":
        return "log-analysis";
      case "soc-analyst-practical-training":
        return "soc-analyst-practical";
      case "incident-response-fundamentals":
        return "incident-response";
      case "detection-engineering-basics":
        return "detection-engineering";
      case "malware-analysis-fundamentals":
        return "malware-analysis";
      case "threat-hunting-fundamentals":
        return "threat-hunting";
      case "soc-analyst-path":
        return "soc-analyst-path";
      case "network-fundamentals":
        return "network-fundamentals";
      case "network-security-monitoring":
        return "network-security-monitoring";
      default:
        return slug;
    }
  }, [slug]);

  const lessonsCourseId = useMemo(() => {
    if (!slug) return "";

    switch (slug) {
      case "blue-team-soc-fundamentals":
        return "soc-fundamentals";
      case "log-analysis-for-beginners":
        return "log-analysis";
      case "soc-analyst-practical-training":
        return "soc-analyst-practical";
      case "incident-response-fundamentals":
        return "incident-response";
      case "detection-engineering-basics":
        return "detection-engineering";
      case "malware-analysis-fundamentals":
        return "malware-analysis";
      case "threat-hunting-fundamentals":
        return "threat-hunting";
      case "soc-analyst-path":
        return "soc-analyst-path";
      case "network-fundamentals":
        return "network-fundamentals";
      case "network-security-monitoring":
        return "network-security-monitoring";
      default:
        return slug;
    }
  }, [slug]);

  const course = getCourseById(courseIdForMeta);

  // Get all lessons flattened for navigation
  const allLessons = useMemo(() => {
    if (!course) return [];
    return course.modules.flatMap((module) => 
      module.lessons.map((lesson) => ({
        ...lesson,
        moduleId: module.id,
        moduleTitle: module.title
      }))
    );
  }, [course]);

  // Find current lesson index
  const currentLessonIndex = allLessons.findIndex((l) => l.id === lessonId);
  const currentLesson =
    currentLessonIndex >= 0 ? allLessons[currentLessonIndex] : null;

  const displayedLessonContent = useMemo(() => {
    if (!lessonContent?.content) return lessonContent;
    if (!currentLesson?.title) return lessonContent;

    const normalize = (value: string) =>
      value
        .toLowerCase()
        .replace(/\s+/g, " ")
        .replace(/\s*[:\-–—]+\s*$/g, "")
        .trim();

    const lines = lessonContent.content.split("\n");
    const firstNonEmptyIndex = lines.findIndex((line) => line.trim().length > 0);
    if (firstNonEmptyIndex < 0) return lessonContent;

    const firstLine = lines[firstNonEmptyIndex];
    const headingMatch = firstLine.match(/^#{1,6}\s+(.+)$/);
    if (!headingMatch) return lessonContent;

    const headingText = headingMatch[1].trim();
    if (normalize(headingText) !== normalize(currentLesson.title)) return lessonContent;

    const nextIndex = firstNonEmptyIndex + 1;
    const shouldRemoveNextBlank = nextIndex < lines.length && lines[nextIndex].trim() === "";
    const filtered = lines.filter((_, idx) => {
      if (idx === firstNonEmptyIndex) return false;
      if (shouldRemoveNextBlank && idx === nextIndex) return false;
      return true;
    });

    return {
      ...lessonContent,
      content: filtered.join("\n"),
    };
  }, [lessonContent, currentLesson?.title]);

  const currentModuleIndex = useMemo(() => {
    if (!course || !lessonId) return -1;
    return course.modules.findIndex((m) => m.lessons.some((l) => l.id === lessonId));
  }, [course, lessonId]);

  const currentModule = currentModuleIndex >= 0 ? course?.modules[currentModuleIndex] : null;
  const currentLessonIndexInModule = useMemo(() => {
    if (!currentModule || !lessonId) return -1;
    return currentModule.lessons.findIndex((l) => l.id === lessonId);
  }, [currentModule, lessonId]);

  const nextLessonInModule =
    currentModule && currentLessonIndexInModule >= 0
      ? currentModule.lessons[currentLessonIndexInModule + 1] ?? null
      : null;

  const prevLessonInModule =
    currentModule && currentLessonIndexInModule > 0
      ? currentModule.lessons[currentLessonIndexInModule - 1] ?? null
      : null;

  const nextModuleFirstLesson =
    course && currentModuleIndex >= 0
      ? course.modules[currentModuleIndex + 1]?.lessons?.[0] ?? null
      : null;

  const moduleQuizId = currentModule?.quizId ?? null;
  const moduleQuizScore = moduleQuizId ? getStoredQuizScore(moduleQuizId) : null;
  const hasPassedModuleQuiz = moduleQuizId ? moduleQuizScore != null && moduleQuizScore >= 70 : true;

  const nextLesson = nextLessonInModule ?? nextModuleFirstLesson;
  const prevLesson = prevLessonInModule ?? null;

  const isCourseProgressEnabled = useMemo(() => {
    if (!slug) return false;
    return Boolean(course);
  }, [slug]);

  const completedCount = allLessons.filter((l) => completedLessonIds.includes(l.id)).length;
  const progressPercent = allLessons.length
    ? Math.round((completedCount / allLessons.length) * 100)
    : 0;

  const courseBgImage = useMemo(() => {
    if (slug && courseBackgrounds[slug]) {
      return courseBackgrounds[slug];
    }
    return socFundamentalsBg;
  }, [slug]);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [lessonId]);

  useEffect(() => {
    const accessToken = localStorage.getItem("accessToken");
    if (!slug) {
      setCompletedLessonIds([]);
      return;
    }

    const fetchProgress = async () => {
      try {
        if (!accessToken) {
          setCompletedLessonIds([]);
          setProgressLoaded(true);
          return;
        }

        const res = await fetch(apiUrl(`/api/courses/${slug}/progress/`), {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });

        if (res.status === 401) {
          localStorage.removeItem("accessToken");
          localStorage.removeItem("refreshToken");
          localStorage.removeItem("userEmail");
          navigate(`/auth?redirect=${encodeURIComponent(`/courses/${slug}/lesson/${lessonId}`)}`);
          return;
        }

        if (res.ok) {
          const data: any[] = await res.json();
          const backendIds = data
            .map((item) =>
              item && item.lesson_id != null ? String(item.lesson_id) : null,
            )
            .filter((id: string | null): id is string => Boolean(id));

          setCompletedLessonIds(backendIds);
        } else {
          setCompletedLessonIds([]);
        }
        
        setProgressLoaded(true);
      } catch {
        // best-effort; if it fails, keep existing state
        setProgressLoaded(true);
      }
    };

    fetchProgress();
  }, [slug]);

  useEffect(() => {
    if (currentLesson && completedLessonIds.includes(currentLesson.id)) {
      setIsCompleted(true);
    } else {
      setIsCompleted(false);
    }
  }, [currentLesson?.id, completedLessonIds]);

  const markLessonComplete = async (): Promise<boolean> => {
    if (!slug || !lessonId || markingComplete || isCompleted) return false;

    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken && TESTING_MODE) {
      // Local testing only — no real backend call, just mirror the same
      // localStorage/UI state the real completion flow sets on success.
      setIsCompleted(true);
      setCompletedLessonIds((prev) =>
        prev.includes(lessonId) ? prev : [...prev, lessonId]
      );
      const completedKey = `completed_lessons_${slug}`;
      const stored = JSON.parse(localStorage.getItem(completedKey) || "[]") as string[];
      if (!stored.includes(lessonId)) {
        localStorage.setItem(completedKey, JSON.stringify([...stored, lessonId]));
      }
      return true;
    }
    if (!accessToken) {
      navigate(`/auth?redirect=${encodeURIComponent(`/courses/${slug}/lesson/${lessonId}`)}`);
      return false;
    }

    try {
      setMarkingComplete(true);

      const res = await fetch(apiUrl(`/api/courses/${slug}/lessons/${lessonId}/complete/`), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });

      if (res.status === 401) {
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
        localStorage.removeItem("userEmail");
        navigate(`/auth?redirect=${encodeURIComponent(`/courses/${slug}/lesson/${lessonId}`)}`);
        return false;
      }

      if (!res.ok) {
        return false;
      }

      setIsCompleted(true);
      setCompletedLessonIds((prev) =>
        prev.includes(lessonId) ? prev : [...prev, lessonId]
      );

      const completedKey = `completed_lessons_${slug}`;
      const stored = JSON.parse(localStorage.getItem(completedKey) || "[]") as string[];
      if (!stored.includes(lessonId)) {
        localStorage.setItem(completedKey, JSON.stringify([...stored, lessonId]));
      }

      if (course && currentLesson) {
        logActivity('lesson', currentLesson.title, course.title);
      }

      return true;
    } catch (err) {
      return false;
    } finally {
      setMarkingComplete(false);
    }
  };

  useEffect(() => {
    if (!isCourseProgressEnabled || !currentLesson || !progressLoaded) return;
    // Never auto-complete quiz lessons — completion is handled by QuizPage on pass
    if (currentLesson.title.toLowerCase().includes('quiz')) return;

    if (!completedLessonIds.includes(currentLesson.id)) {
      const timer = setTimeout(() => {
        void markLessonComplete();
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [currentLesson?.id, isCourseProgressEnabled, progressLoaded]);

  // ─── Gate check: wait for progress to load before evaluating ───
  useEffect(() => {
    if (!slug || !lessonId || !course || !progressLoaded) return;
    if (isStaff) return;

    const currentModuleIndex = course.modules.findIndex((m) =>
      m.lessons.some((l) => l.id === lessonId),
    );
    if (currentModuleIndex <= 0) return;

    const previousModule = course.modules[currentModuleIndex - 1];

    const gateQuizId = getModuleGateQuizId(previousModule);
    if (!gateQuizId) return;

    // Pass if quiz score ≥70 OR the quiz lesson itself is in completedLessonIds
    const score = getStoredQuizScore(gateQuizId);
    const passedByScore = score != null && score >= 70;
    const passedByCompletion = completedLessonIds.includes(gateQuizId);

    // Backward compat: also check by the quiz lesson's raw ID in the previous module
    // (covers stored scores from before quizId mapping was corrected)
    const prevQuizLesson = previousModule.lessons.find((l) =>
      l.title.toLowerCase().includes("quiz"),
    );
    const prevQuizLessonScore = prevQuizLesson ? getStoredQuizScore(prevQuizLesson.id) : null;
    const passedByLessonScore = prevQuizLessonScore != null && prevQuizLessonScore >= 70;
    const passedByLessonCompletion = prevQuizLesson
      ? completedLessonIds.includes(prevQuizLesson.id)
      : false;

    // Backward compat: also check quizId+1 (old off-by-one cascade from prior bug)
    // e.g. module 8 was q8 before fix, now q7 — score stored at q8 still counts
    const oldQuizNum = parseInt(gateQuizId.replace("q", ""), 10);
    const oldGateQuizId = isNaN(oldQuizNum) ? null : `q${oldQuizNum + 1}`;
    const oldScore = oldGateQuizId ? getStoredQuizScore(oldGateQuizId) : null;
    const passedByOldScore = oldScore != null && oldScore >= 70;
    const passedByOldCompletion = oldGateQuizId ? completedLessonIds.includes(oldGateQuizId) : false;

    if (passedByScore || passedByLessonScore || passedByOldScore || passedByCompletion || passedByLessonCompletion || passedByOldCompletion) return;

    // Redirect to the previous module quiz
    navigate(`/courses/${slug}/quiz/${gateQuizId}`, { replace: true });
  }, [slug, lessonId, course, progressLoaded, completedLessonIds, isStaff, navigate]);

  // These must stay above early-returns so hook count is stable across renders
  const quizScoreData = useMemo(() => {
    if (!slug || !lessonId) return null;
    const rawKey = `quiz_${slug}_${lessonContent?.quiz || lessonId}`;
    const resolvedId = resolveQuizStorageId(lessonContent?.quiz || lessonId || "");
    const resolvedKey = `quiz_${slug}_${resolvedId}`;
    const score = localStorage.getItem(rawKey) ?? localStorage.getItem(resolvedKey);
    return { score, hasScore: score !== null };
  }, [slug, lessonId, lessonContent?.quiz]);

  const isQuizLesson = useMemo(() => {
    return Boolean(lessonContent?.quiz) ||
      Boolean(currentLesson?.title.toLowerCase().includes('quiz'));
  }, [lessonContent?.quiz, currentLesson?.title]);

  if (!course) {
    console.warn('LessonViewer redirect: course not found, going back to /courses');
    return <Navigate to="/courses" replace />;
  }

  // ── Gate 1: enrollment check (RS256 + user binding) ──────────────────────
  if (accessState === "loading") {
    return (
      <main className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-muted-foreground">Verifying access...</p>
      </main>
    );
  }
  if (accessState === "unauthenticated") {
    return <Navigate to={`/auth?redirect=${encodeURIComponent(location.pathname)}`} replace />;
  }
  if (accessState === "denied") {
    // Not enrolled or not paid — send to course page where they can purchase.
    return <Navigate to={`/courses/${slug}`} replace />;
  }

  // ── Gate 2: lesson content loading ────────────────────────────────────────
  // Only shows while the backend responds; sessionStorage cache makes this
  // instant on subsequent navigations within the same session.
  if (contentLoading) {
    return (
      <main className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-muted-foreground">Loading lesson...</p>
      </main>
    );
  }

  if (!lessonId || !currentLesson) {
    console.warn('LessonViewer redirect: lesson not found, going back to course page', {
      slug,
      lessonId,
      hasCourse: !!course,
      allLessonsIds: allLessons.map(l => l.id),
    });
    return <Navigate to={`/courses/${slug}`} replace />;
  }

  const navigateToLesson = (newLessonId: string): boolean => {
    if (!slug || !course) return false;

    const targetModuleIndex = course.modules.findIndex((m) =>
      m.lessons.some((l) => l.id === newLessonId),
    );
    if (!isStaff && targetModuleIndex > 0) {
      const isMovingToDifferentModule = targetModuleIndex !== currentModuleIndex;

      if (isMovingToDifferentModule) {
        const previousModule = course.modules[targetModuleIndex - 1];
        const gateQuizId = getModuleGateQuizId(previousModule);
        if (gateQuizId) {
          const score = getStoredQuizScore(gateQuizId);
          const passedByScore = score != null && score >= 70;
          const passedByCompletion = completedLessonIds.includes(gateQuizId);

          // Backward compat: also check by the quiz lesson's raw ID
          const prevQuizLesson = previousModule.lessons.find((l) =>
            l.title.toLowerCase().includes("quiz"),
          );
          const prevQuizLessonScore = prevQuizLesson ? getStoredQuizScore(prevQuizLesson.id) : null;
          const passedByLessonScore = prevQuizLessonScore != null && prevQuizLessonScore >= 70;
          const passedByLessonCompletion = prevQuizLesson
            ? completedLessonIds.includes(prevQuizLesson.id)
            : false;

          // Backward compat: also check quizId+1 (old off-by-one cascade from prior bug)
          const oldQuizNum = parseInt(gateQuizId.replace("q", ""), 10);
          const oldGateQuizId = isNaN(oldQuizNum) ? null : `q${oldQuizNum + 1}`;
          const oldScore = oldGateQuizId ? getStoredQuizScore(oldGateQuizId) : null;
          const passedByOldScore = oldScore != null && oldScore >= 70;
          const passedByOldCompletion = oldGateQuizId ? completedLessonIds.includes(oldGateQuizId) : false;

          if (!passedByScore && !passedByLessonScore && !passedByOldScore && !passedByCompletion && !passedByLessonCompletion && !passedByOldCompletion) {
            window.alert("Complete the quiz (70%+) to unlock the next module.");
            navigate(`/courses/${slug}/quiz/${gateQuizId}`);
            return false;
          }
        }
      }
    }

    const targetLesson = course.modules[targetModuleIndex]?.lessons?.find(l => l.id === newLessonId);
    const isTargetQuizLesson = targetLesson?.title.toLowerCase().includes('quiz') ?? false;

    if (isTargetQuizLesson && currentModuleIndex === targetModuleIndex) {
      navigate(`/courses/${slug}/lesson/${newLessonId}`);
      return true;
    }

    navigate(`/courses/${slug}/lesson/${newLessonId}`);
    return true;
  };

  // Parse markdown-like content to JSX
  const renderContent = (content: string) => {
    const lines = content.trim().split('\n');
    const elements: JSX.Element[] = [];
    let inCodeBlock = false;
    let codeBlockContent: string[] = [];
    let codeBlockLang = '';
    let inTable = false;
    let tableRows: string[][] = [];
    let listItems: string[] = [];
    let inList = false;

    const flushList = () => {
      if (listItems.length > 0) {
        elements.push(
          <ul key={`list-${elements.length}`} className="space-y-2 my-4 ml-4">
            {listItems.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2 text-muted-foreground">
                <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
                <span dangerouslySetInnerHTML={{ __html: parseInlineFormatting(item) }} />
              </li>
            ))}
          </ul>
        );
        listItems = [];
      }
      inList = false;
    };

    const flushTable = () => {
      if (tableRows.length > 1) {
        const headers = tableRows[0];
        const body = tableRows.slice(2);
        elements.push(
          <div key={`table-${elements.length}`} className="my-6 overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-white/10">
                  {headers.map((h, i) => (
                    <th key={i} className="text-left py-2 px-3 text-foreground font-medium">{h.trim()}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {body.map((row, rowIdx) => (
                  <tr key={rowIdx} className="border-b border-white/5 hover:bg-white/[0.02]">
                    {row.map((cell, cellIdx) => (
                      <td key={cellIdx} className="py-2 px-3 text-muted-foreground">{cell.trim()}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      }
      tableRows = [];
      inTable = false;
    };

    const parseInlineFormatting = (text: string): string => {
      return text
        .replace(/\*\*(.+?)\*\*/g, '<strong class="text-foreground font-semibold">$1</strong>')
        .replace(/\*(.+?)\*/g, '<em>$1</em>')
        .replace(/`(.+?)`/g, '<code class="px-1.5 py-0.5 rounded bg-muted/50 text-primary text-sm font-mono">$1</code>');
    };

    lines.forEach((line, lineIdx) => {
      if (line.startsWith('```')) {
        if (inCodeBlock) {
          elements.push(
            <pre key={`code-${elements.length}`} className="my-4 p-4 rounded-lg bg-card/50 border border-white/[0.08] overflow-x-auto">
              <code className="text-sm text-muted-foreground font-mono whitespace-pre">
                {codeBlockContent.join('\n')}
              </code>
            </pre>
          );
          codeBlockContent = [];
          inCodeBlock = false;
        } else {
          flushList();
          flushTable();
          codeBlockLang = line.slice(3);
          inCodeBlock = true;
        }
        return;
      }

      if (inCodeBlock) {
        codeBlockContent.push(line);
        return;
      }

      if (line.includes('|') && line.trim().startsWith('|')) {
        flushList();
        if (!inTable) inTable = true;
        const cells = line.split('|').filter(c => c.trim() !== '');
        if (!cells.every(c => c.trim().match(/^[-:]+$/))) {
          tableRows.push(cells);
        } else {
          tableRows.push(cells);
        }
        return;
      } else if (inTable) {
        flushTable();
      }

      if (line.trim() === '') {
        flushList();
        return;
      }

      if (line.startsWith('# ')) {
        flushList();
        elements.push(
          <h1 key={`h1-${lineIdx}`} className="text-2xl md:text-3xl font-bold text-foreground mt-5 mb-2 first:mt-0">
            {line.slice(2)}
          </h1>
        );
        return;
      }
      if (line.startsWith('## ')) {
        flushList();
        elements.push(
          <h2 key={`h2-${lineIdx}`} className="text-xl md:text-2xl font-semibold text-foreground mt-5 mb-2 border-b border-white/10 pb-2">
            {line.slice(3)}
          </h2>
        );
        return;
      }
      if (line.startsWith('### ')) {
        flushList();
        elements.push(
          <h3 key={`h3-${lineIdx}`} className="text-lg font-semibold text-foreground mt-4 mb-1.5">
            {line.slice(4)}
          </h3>
        );
        return;
      }

      if (line.startsWith('> ')) {
        flushList();
        elements.push(
          <blockquote key={`quote-${lineIdx}`} className="my-4 pl-4 border-l-2 border-primary/50 text-muted-foreground italic">
            {line.slice(2)}
          </blockquote>
        );
        return;
      }

      if (line.match(/^[-*] /)) {
        inList = true;
        listItems.push(line.slice(2));
        return;
      }

      if (line.match(/^\d+\. /)) {
        flushList();
        const match = line.match(/^(\d+)\. (.+)$/);
        if (match) {
          elements.push(
            <div key={`num-${lineIdx}`} className="flex items-start gap-3 my-2 text-muted-foreground">
              <span className="text-primary font-medium">{match[1]}.</span>
              <span dangerouslySetInnerHTML={{ __html: parseInlineFormatting(match[2]) }} />
            </div>
          );
        }
        return;
      }

      flushList();
      if (line.trim()) {
        elements.push(
          <p 
            key={`p-${lineIdx}`} 
            className="text-muted-foreground leading-relaxed my-2"
            dangerouslySetInnerHTML={{ __html: parseInlineFormatting(line) }}
          />
        );
      }
    });

    flushList();
    flushTable();

    return elements;
  };

  return (
    <main className="min-h-screen bg-background">
      <Navbar />

      <div className="flex pt-20">
        {/* Sidebar */}
        <aside
          className={`fixed left-0 top-16 md:top-20 h-[calc(100vh-4rem)] md:h-[calc(100vh-5rem)] bg-card/95 md:bg-card/30 backdrop-blur-lg border-r border-white/[0.08] transition-all duration-300 z-40 ${
            sidebarOpen ? 'w-full md:w-80' : 'w-0'
          }`}
        >
          {sidebarOpen && (
            <ScrollArea className="h-full">
              <div className="p-4">
                {/* Course Header */}
                <Link to={`/courses/${slug}`} className="flex items-center gap-3 mb-6 group">
                  <div className="w-10 h-10 rounded-lg bg-primary/15 border border-primary/25 flex items-center justify-center">
                    <div className="w-5 h-5 rounded-full bg-primary/40" />
                  </div>
                  <div>
                    <h3 className="text-sm font-semibold text-foreground group-hover:text-primary transition-colors">
                      {course.shortTitle}
                    </h3>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <Progress value={progressPercent} className="w-16 h-1.5" />
                      <span>{progressPercent}%</span>
                    </div>
                  </div>
                </Link>

                {/* Modules */}
                <div className="space-y-2">
                  {course.modules.map((module) => (
                    <div key={module.id}>
                      <div className="px-3 py-2 text-xs font-medium text-muted-foreground uppercase tracking-wider">
                        {formatModuleId(module.id)}. {module.title}
                      </div>
                      <div className="space-y-0.5">
                        {module.lessons.map((lesson) => {
                          const isActive = lesson.id === lessonId;
                          const isCompleted = completedLessonIds.includes(lesson.id);
                          const isLocked = !isActive && !isCompleted && lesson.status === "locked";
                          
                          return (
                            <button
                              key={lesson.id}
                              onClick={() => !isLocked && navigateToLesson(lesson.id)}
                              disabled={isLocked}
                              className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-left text-sm transition-all ${
                                isActive 
                                  ? 'bg-primary/15 text-primary border border-primary/25' 
                                  : isLocked
                                  ? 'text-muted-foreground/40 cursor-not-allowed'
                                  : 'text-muted-foreground hover:text-foreground hover:bg-white/[0.03]'
                              }`}
                            >
                              {isCompleted ? (
                                <CheckCircle className="w-4 h-4 text-primary flex-shrink-0" />
                              ) : isLocked ? (
                                <Lock className="w-4 h-4 flex-shrink-0" />
                              ) : (
                                <div className={`w-4 h-4 rounded-full border-2 flex-shrink-0 ${
                                  isActive ? 'border-primary bg-primary/20' : 'border-muted-foreground/30'
                                }`} />
                              )}
                              <span className="truncate">{lesson.title}</span>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </ScrollArea>
          )}
        </aside>

        {/* Toggle Button */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className={`fixed top-20 md:top-24 z-50 p-2 rounded-r-lg bg-card/50 border border-l-0 border-white/[0.08] text-muted-foreground hover:text-foreground transition-all ${
            sidebarOpen ? 'left-full md:left-80' : 'left-0'
          }`}
        >
          {sidebarOpen ? <ChevronLeft className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
        </button>

        {/* Main Content */}
        <div className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'md:ml-80' : 'ml-0'}`}>
          {/* Lesson Header */}
          <div className="relative">
            <div className="absolute inset-0 h-48 overflow-hidden">
              <div 
                className="absolute inset-0 bg-cover bg-center opacity-20"
                style={{ backgroundImage: `url(${courseBgImage})` }}
              />
              <div className="absolute inset-0 bg-gradient-to-b from-background/50 to-background" />
            </div>

            <div className="relative container mx-auto px-6 py-8">
              {/* Breadcrumb */}
              <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4">
                <Link to="/courses" className="hover:text-primary transition-colors">Courses</Link>
                <ChevronRight className="w-4 h-4" />
                <Link to={`/courses/${slug}`} className="hover:text-primary transition-colors">{course.shortTitle}</Link>
                <ChevronRight className="w-4 h-4" />
                <span className="text-foreground">{currentLesson.title}</span>
              </div>

              {/* Lesson Title */}
              <div className="flex items-center gap-4 mb-2">
                <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-primary/15 text-primary border border-primary/25">
                  Lesson {lessonId}
                </span>
                {currentLesson.duration && (
                  <span className="flex items-center gap-1 text-xs text-muted-foreground">
                    <Clock className="w-3 h-3" />
                    {currentLesson.duration}
                  </span>
                )}
              </div>
              <h1 className="text-2xl md:text-3xl font-bold text-foreground">
                {currentLesson.title}
              </h1>
            </div>
          </div>

          {/* Lesson Content */}
          <div className="container mx-auto px-6 py-8">
            <div className="max-w-4xl">
              {lessonContent ? (
                <>
                  {/* Main Content — skip for quiz lessons (avoids rendering raw Q&A data) */}
                  {!isQuizLesson && (
                    <div className="prose prose-invert max-w-none">
                      {renderContent(displayedLessonContent?.content || "")}
                    </div>
                  )}

                  {/* Quiz Button for Quiz Lessons */}
                  {isQuizLesson && (
                    <div className="mt-8 p-6 rounded-xl bg-orange-500/10 border border-orange-500/20">
                      <div className="flex items-center gap-3 mb-4">
                        <FileQuestion className="w-6 h-6 text-orange-400" />
                        <h3 className="text-lg font-semibold text-foreground">Ready to Test Your Knowledge?</h3>
                      </div>
                      <p className="text-muted-foreground mb-6">
                        This quiz covers the material from the previous lessons. You need to score 70% or higher to unlock the next module.
                      </p>
                      
                      {/* Quiz Score Display */}
                      <div className="mb-6 p-4 rounded-lg bg-background/50 border border-white/[0.08]">
                        <div className="text-center">
                          <h4 className="text-sm font-medium text-muted-foreground mb-2">Your Quiz Score</h4>
                          <div className="text-2xl font-bold text-foreground mb-1">
                            {quizScoreData?.score ? `${quizScoreData.score}%` : 'Not taken yet'}
                          </div>
                          <div className="text-xs text-muted-foreground">
                            {(() => {
                              const score = quizScoreData?.score;
                              if (!score) return 'Complete the quiz to see your score';
                              const scoreNum = parseInt(score);
                              if (scoreNum >= 70) return '✅ Passed - Ready for next module!';
                              return '❌ Need 70% to pass - Try again!';
                            })()}
                          </div>
                        </div>
                      </div>
                      
                      <Button
                        onClick={() => navigate(`/courses/${slug}/quiz/${lessonContent?.quiz || lessonId}`)}
                        className="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3"
                      >
                        <FileQuestion className="w-4 h-4 mr-2" />
                        {quizScoreData?.hasScore ? 'Retake Quiz' : 'Start Quiz'}
                      </Button>
                    </div>
                  )}

                  {/* Key Takeaways */}
                  {lessonContent.keyTakeaways && lessonContent.keyTakeaways.length > 0 && (
                    <div className="mt-12 p-6 rounded-xl bg-primary/5 border border-primary/20">
                      <div className="flex items-center gap-2 mb-4">
                        <Lightbulb className="w-5 h-5 text-primary" />
                        <h3 className="text-lg font-semibold text-foreground">Key Takeaways</h3>
                      </div>
                      <ul className="space-y-2">
                        {lessonContent.keyTakeaways.map((takeaway, idx) => (
                          <li key={idx} className="flex items-start gap-2 text-muted-foreground">
                            <CheckCircle className="w-4 h-4 text-primary mt-0.5 flex-shrink-0" />
                            <span>{takeaway}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Practical Exercise */}
                  {lessonContent.practicalExercise && (
                    <div className="mt-8 p-6 rounded-xl bg-secondary/5 border border-secondary/20">
                      <div className="flex items-center gap-2 mb-4">
                        <FlaskConical className="w-5 h-5 text-secondary" />
                        <h3 className="text-lg font-semibold text-foreground">
                          Practical Exercise: {lessonContent.practicalExercise.title}
                        </h3>
                      </div>
                      <p className="text-muted-foreground mb-4">{lessonContent.practicalExercise.description}</p>
                      <ol className="space-y-2 mb-6">
                        {lessonContent.practicalExercise.steps.map((step, idx) => (
                          <li key={idx} className="flex items-start gap-3 text-muted-foreground">
                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-secondary/20 text-secondary text-sm flex items-center justify-center">
                              {idx + 1}
                            </span>
                            <span>{step}</span>
                          </li>
                        ))}
                      </ol>

                      {lessonContent.practicalExercise.labQuestions && lessonContent.practicalExercise.labQuestions.length > 0 && (
                        <LabQuestionsSection
                          scenario={lessonContent.practicalExercise.labScenario}
                          questions={lessonContent.practicalExercise.labQuestions}
                          slug={slug!}
                          lessonId={lessonId!}
                        />
                      )}
                    </div>
                  )}

                  {/* Additional Resources */}
                  {lessonContent.additionalResources && lessonContent.additionalResources.length > 0 && (
                    <div className="mt-8 p-6 rounded-xl bg-card/25 border border-white/[0.08]">
                      <div className="flex items-center gap-2 mb-4">
                        <BookOpen className="w-5 h-5 text-primary" />
                        <h3 className="text-lg font-semibold text-foreground">Additional Resources</h3>
                      </div>
                      <div className="space-y-2">
                        {lessonContent.additionalResources.map((resource, idx) => (
                          <a
                            key={idx}
                            href={resource.url || "#"}
                            target={resource.url ? "_blank" : undefined}
                            rel="noopener noreferrer"
                            className="flex items-center justify-between p-3 rounded-lg bg-card/30 border border-white/[0.06] hover:bg-card/50 transition-colors group"
                          >
                            <div className="flex items-center gap-3">
                              <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
                                {resource.type === "video" && <BookOpen className="w-4 h-4 text-primary" />}
                                {resource.type === "article" && <BookOpen className="w-4 h-4 text-primary" />}
                                {resource.type === "tool" && <BookOpen className="w-4 h-4 text-secondary" />}
                                {resource.type === "documentation" && <BookOpen className="w-4 h-4 text-blue-400" />}
                              </div>
                              <div>
                                <span className="text-foreground group-hover:text-primary transition-colors">{resource.title}</span>
                                <span className="ml-2 text-xs text-muted-foreground capitalize">({resource.type})</span>
                              </div>
                            </div>
                            {resource.url && <ExternalLink className="w-4 h-4 text-muted-foreground" />}
                          </a>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              ) : isQuizLesson ? (
                <div className="mt-8 p-6 rounded-xl bg-orange-500/10 border border-orange-500/20">
                  <div className="flex items-center gap-3 mb-4">
                    <FileQuestion className="w-6 h-6 text-orange-400" />
                    <h3 className="text-lg font-semibold text-foreground">Ready to Test Your Knowledge?</h3>
                  </div>
                  <p className="text-muted-foreground mb-6">
                    This quiz covers the material from the previous lessons. You need to score 70% or higher to unlock the next module.
                  </p>
                  <div className="mb-6 p-4 rounded-lg bg-background/50 border border-white/[0.08]">
                    <div className="text-center">
                      <h4 className="text-sm font-medium text-muted-foreground mb-2">Your Quiz Score</h4>
                      <div className="text-2xl font-bold text-foreground mb-1">
                        {quizScoreData?.score ? `${quizScoreData.score}%` : 'Not taken yet'}
                      </div>
                      <div className="text-xs text-muted-foreground">
                        {(() => {
                          const score = quizScoreData?.score;
                          if (!score) return 'Complete the quiz to see your score';
                          const scoreNum = parseInt(score);
                          if (scoreNum >= 70) return '✅ Passed - Ready for next module!';
                          return '❌ Need 70% to pass - Try again!';
                        })()}
                      </div>
                    </div>
                  </div>
                  <Button
                    onClick={() => navigate(`/courses/${slug}/quiz/${lessonId}`)}
                    className="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3"
                  >
                    <FileQuestion className="w-4 h-4 mr-2" />
                    {quizScoreData?.hasScore ? 'Retake Quiz' : 'Start Quiz'}
                  </Button>
                </div>
              ) : (
                <div className="text-center py-16">
                  <BookOpen className="w-12 h-12 text-muted-foreground/30 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-foreground mb-2">Content Coming Soon</h3>
                  <p className="text-muted-foreground">
                    The content for this lesson is currently being developed.
                  </p>
                </div>
              )}

              {/* Navigation */}
              <div className="mt-12 pt-8 border-t border-white/[0.08] flex items-center justify-between">
                {prevLesson ? (
                  <button
                    onClick={() => navigateToLesson(prevLesson.id)}
                    className="flex items-center gap-2 px-4 py-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-white/[0.03] transition-colors"
                  >
                    <ChevronLeft className="w-4 h-4" />
                    <div className="text-left">
                      <div className="text-xs text-muted-foreground">Previous</div>
                      <div className="text-sm">{prevLesson.title}</div>
                    </div>
                  </button>
                ) : (
                  <div />
                )}

                {isCourseProgressEnabled ? (
                  nextLesson ? (
                    <button
                      onClick={() => {
                        if (nextLessonInModule?.id) {
                          const didNavigate = navigateToLesson(nextLessonInModule.id);
                          if (didNavigate && !isQuizLesson) {
                            void markLessonComplete();
                          }
                          return;
                        }

                        if (moduleQuizId && !hasPassedModuleQuiz) {
                          // Never mark a quiz lesson complete via Next — only QuizPage does that on pass
                          if (!isQuizLesson) void markLessonComplete();
                          navigate(`/courses/${slug}/quiz/${moduleQuizId}`);
                          return;
                        }

                        if (nextModuleFirstLesson?.id) {
                          const didNavigate = navigateToLesson(nextModuleFirstLesson.id);
                          if (didNavigate && !isQuizLesson) {
                            void markLessonComplete();
                          }
                          return;
                        }

                        if (!isQuizLesson) void markLessonComplete();
                        navigate(`/courses/${slug}`);
                      }}
                      className="flex items-center gap-2 px-4 py-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-white/[0.03] transition-colors"
                    >
                      <div className="text-right">
                        <div className="text-xs text-muted-foreground">Next</div>
                        <div className="text-sm">{nextLesson.title}</div>
                      </div>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  ) : (
                    <button
                      onClick={() => {
                        if (!isQuizLesson) void markLessonComplete();
                        navigate(`/courses/${slug}`);
                      }}
                      className="flex items-center gap-2 px-4 py-2 rounded-lg text-primary hover:bg-primary/10 transition-colors"
                    >
                      <span>Back to Course</span>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  )
                ) : (
                  nextLesson ? (
                    <button
                      disabled
                      className="flex items-center gap-2 px-4 py-2 rounded-lg text-muted-foreground/40 cursor-not-allowed border border-dashed border-muted/30"
                    >
                      <div className="text-right">
                        <div className="text-xs text-muted-foreground/60">Next</div>
                        <div className="text-sm">Coming soon</div>
                      </div>
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  ) : (
                    <span />
                  )
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default LessonViewer;