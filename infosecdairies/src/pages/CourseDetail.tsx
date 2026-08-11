import { useEffect, useMemo, useState, useCallback } from "react";
import { Link, useParams, Navigate, useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import {
  ChevronLeft,
  ChevronDown,
  Lock,
  CheckCircle,
  BookOpen,
  FileQuestion,
  FolderOpen,
  ArrowRight,
  Clock,
  FileText,
  Link as LinkIcon,
  Download,
  ExternalLink,
} from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { useAuth } from "@/context/AuthContext";
import { useCurrency } from "@/context/CurrencyContext";
import { useCourseAccess } from "@/hooks/useCourseAccess";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { courses as staticCourses, getCoursePriceInr } from "@/data/courses";
import { apiUrl, fetchCourseBySlug } from "../services/api";
import { TESTING_MODE } from "@/lib/testingMode";
import QRCode from "qrcode";

// Import all course background images
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
  "log-analysis-for-beginners": logAnalysisBg,
  "siem-fundamentals": siemFundamentalsBg,
  "soc-analyst-practical-training": socAnalystPracticalBg,
  "incident-response-fundamentals": incidentResponseBg,
  "threat-hunting-fundamentals": threatHuntingBg,
  "detection-engineering-basics": detectionEngineeringBg,
  "malware-analysis-fundamentals": malwareAnalysisBg,
  "network-fundamentals": networkFundamentalsBg,
};

const certificateTemplatesBySlug: Record<string, string> = {
  "blue-team-soc-fundamentals": "/certs/cc/blue team soc analyst.png",
  "detection-engineering-basics": "/certs/cc/Detection Engineering Basics course copy.png",
  "incident-response-fundamentals": "/certs/cc/Incident Response course copy.png",
  "log-analysis-for-beginners": "/certs/cc/Log Analysis for Beginners course copy.png",
  "malware-analysis-fundamentals": "/certs/cc/Malware Analysis Fundamentals Courses copy.png",
  "network-fundamentals": "/certs/cc/network fundaments.png",
  "network-security-monitoring": "/certs/cc/Network Security Monitoring course copy.jpg",
  "siem-fundamentals": "/certs/cc/SIEM Fundamentals course copy.jpg",
  "soc-analyst-path": "/certs/cc/soc analyst learing path.png",
  "threat-hunting-fundamentals": "/certs/cc/Threat Hunting Fundamentals course copy.png",
};

const wrapText = (
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number,
  y: number,
  maxWidth: number,
  lineHeight: number,
) => {
  const words = text.split(/\s+/).filter(Boolean);
  let line = "";
  let currentY = y;

  for (let i = 0; i < words.length; i++) {
    const testLine = line ? `${line} ${words[i]}` : words[i];
    const metrics = ctx.measureText(testLine);
    if (metrics.width > maxWidth && line) {
      ctx.fillText(line, x, currentY);
      line = words[i];
      currentY += lineHeight;
    } else {
      line = testLine;
    }
  }

  if (line) ctx.fillText(line, x, currentY);
};

const difficultyLabels = {
  easy: "Beginner",
  medium: "Intermediate",
  hard: "Advanced",
};

// Helper function to map slugs to course IDs
const getCourseIdFromSlug = (slug: string): string => {
  switch (slug) {
    case "blue-team-soc-fundamentals":
      return "soc-fundamentals";
    case "log-analysis-for-beginners":
      return "log-analysis";
    case "siem-fundamentals":
      return "siem-fundamentals";
    case "soc-analyst-practical-training":
      return "soc-analyst-practical";
    case "incident-response-fundamentals":
      return "incident-response";
    case "threat-hunting-fundamentals":
      return "threat-hunting";
    case "detection-engineering-basics":
      return "detection-engineering";
    case "malware-analysis-fundamentals":
      return "malware-analysis";
    case "soc-analyst-path":
      return "soc-analyst-path";
    case "network-fundamentals":
      return "network-fundamentals";
    case "network-security-monitoring":
      return "network-security-monitoring";
    default:
      return slug; // fallback to slug if no mapping exists
  }
};

const CourseDetail = () => {
  const { slug } = useParams<{ slug: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { symbol, prices } = useCurrency();

  const [courseMeta, setCourseMeta] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"modules" | "resources">(
    "modules"
  );
  const [openModules, setOpenModules] = useState<string[]>(["1", "2"]);

  // Only some courses are fully implemented with enrollment/progress
  // Must be declared before useCourseAccess which depends on it
  const isCourseProgressEnabled = useMemo(() => {
    if (!slug) return false;
    return staticCourses.some(
      (c) => c.id === slug || c.id === getCourseIdFromSlug(slug)
    );
  }, [slug]);

  // Secure enrollment gate — backed by RS256-signed token verified locally.
  // Intercepting + modifying the API response cannot grant access because
  // the RSA signature check will reject any tampered token.
  const { accessState, recheck: recheckAccess } = useCourseAccess(
    isCourseProgressEnabled ? slug : undefined
  );
  const isEnrolled = accessState === "granted";
  const checkingEnrollment = accessState === "loading";
  const [enrollLoading, setEnrollLoading] = useState(false);
  const [enrollError, setEnrollError] = useState<string | null>(null);
  const [completedLessonIds, setCompletedLessonIds] = useState<string[]>([]);
  const [quizScores, setQuizScores] = useState<Record<string, number>>({});
  // null = not yet fetched, true/false = server response
  const [serverCompleted, setServerCompleted] = useState<boolean | null>(null);
  const [showShareModal, setShowShareModal] = useState(false);
  const [shareModalText, setShareModalText] = useState("");
  const [shareModalUrl, setShareModalUrl] = useState("");
  const [copied, setCopied] = useState(false);

  // Frozen cert metadata fetched from server — name/date are locked at generation time.
  interface CertMeta {
    exists: boolean;
    studentName: string;
    issueDate: string; // ISO "YYYY-MM-DD"
    certId?: string;
    courseName?: string;
  }
  const [certMeta, setCertMeta] = useState<CertMeta | null>(null);
  const [isCertDownloading, setIsCertDownloading] = useState(false);

  const displayPriceInr = useMemo(() => {
    if (!slug) return null;
    const course = staticCourses.find((c) => c.id === slug || c.id === getCourseIdFromSlug(slug));
    if (!course) return null;
    return getCoursePriceInr(slug, course.difficulty);
  }, [slug]);

  const isPaidCourse = useMemo(() => {
    return (
      Boolean(isCourseProgressEnabled) &&
      typeof displayPriceInr === "number" &&
      displayPriceInr > 0
    );
  }, [displayPriceInr, isCourseProgressEnabled]);

  // Display price in user's local currency (from CurrencyContext) keyed by difficulty
  const displayPrice = useMemo(() => {
    if (typeof displayPriceInr !== "number" || displayPriceInr === 0) return displayPriceInr;
    const difficulty = staticCourses.find(
      (c) => c.id === slug || c.id === getCourseIdFromSlug(slug ?? "")
    )?.difficulty;
    if (difficulty === "easy") return prices.easy;
    if (difficulty === "medium") return prices.medium;
    if (difficulty === "hard") return prices.hard;
    return displayPriceInr;
  }, [displayPriceInr, prices, slug]);

  const isLockedForPayment = isPaidCourse && !isEnrolled;

  const effectiveCompletedLessonIds = !isEnrolled || isLockedForPayment ? [] : completedLessonIds;
  const effectiveQuizScores = !isEnrolled || isLockedForPayment ? ({} as Record<string, number>) : quizScores;

  useEffect(() => {
    if (!slug) return;

    const loadCourse = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log('Loading course for slug:', slug);
        const data = await fetchCourseBySlug(slug); // calls `${VITE_API_BASE_URL}/api/courses/${slug}/`
        console.log('Course data from API:', data);
        setCourseMeta(data);
      } catch (err) {
        console.error('Error loading course:', err);
        // If backend doesn't have this slug, still allow rendering from staticCourses
        setCourseMeta(null);
        setError(null);
      } finally {
        setLoading(false);
      }
    };

    loadCourse();
  }, [slug]);

  // Load quiz scores from localStorage
  useEffect(() => {
    if (!slug) return;
    
    const scores: Record<string, number> = {};
    
    // Check for quiz scores in localStorage
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith(`quiz_${slug}_`)) {
        const quizId = key.replace(`quiz_${slug}_`, '');
        const score = parseInt(localStorage.getItem(key) || '0');
        scores[quizId] = score;
      }
    }
    
    setQuizScores(scores);
  }, [slug]);

  // Fetch server-authoritative completion status for certificate gating.
  // The server checks QuizScore records — impossible to fake via localStorage.
  useEffect(() => {
    if (!slug || !user) return;
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) return;

    fetch(apiUrl(`/api/courses/${slug}/completion/`), {
      headers: { Authorization: `Bearer ${accessToken}` },
    })
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (data && typeof data.completed === "boolean") {
          setServerCompleted(data.completed);
        }
      })
      .catch(() => {});
  }, [slug, user]);

  // Listen for quiz completion events and re-check server completion
  useEffect(() => {
    const handleQuizCompleted = (event: CustomEvent) => {
      const { quizId, score, passed } = event.detail;
      setQuizScores(prev => ({
        ...prev,
        [quizId]: score
      }));
      
      // If quiz was passed, also mark it as completed locally and re-check server
      if (passed) {
        setCompletedLessonIds(prev => {
          if (!prev.includes(quizId)) {
            return [...prev, quizId];
          }
          return prev;
        });
        // Re-fetch server completion so certificate unlocks immediately after passing
        const accessToken = localStorage.getItem("accessToken");
        if (accessToken && slug) {
          fetch(apiUrl(`/api/courses/${slug}/completion/`), {
            headers: { Authorization: `Bearer ${accessToken}` },
          })
            .then((r) => (r.ok ? r.json() : null))
            .then((data) => {
              if (data && typeof data.completed === "boolean") {
                setServerCompleted(data.completed);
              }
            })
            .catch(() => {});
        }
      }
    };

    window.addEventListener('quizCompleted', handleQuizCompleted as EventListener);

    return () => {
      window.removeEventListener('quizCompleted', handleQuizCompleted as EventListener);
    };
  }, []);

  // Fetch frozen cert metadata (name + completion date) from the server.
  // This runs once per course visit so we always use the server-locked values.
  useEffect(() => {
    if (!slug || !user) return;
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) return;
    fetch(apiUrl(`/api/certificates/my/${slug}/`), {
      headers: { Authorization: `Bearer ${accessToken}` },
    })
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (data) {
          setCertMeta({
            exists: data.exists,
            studentName: data.studentName,
            issueDate: data.issueDate,
            certId: data.certId,
            courseName: data.courseName,
          });
        }
      })
      .catch(() => {});
  }, [slug, user]);

  // Enrollment is now handled by useCourseAccess (RS256-verified) above.

  const staticCourse = useMemo(
    () =>
      staticCourses.find(
        (c) => c.id === slug || c.id === getCourseIdFromSlug(slug) || (courseMeta && c.title === courseMeta.title)
      ),
    [slug, courseMeta]
  );

  console.log('Static course found:', staticCourse);
  console.log('Course meta:', courseMeta);
  console.log('Slug:', slug);

  const levelToDifficulty: Record<string, "easy" | "medium" | "hard"> = {
    beginner: "easy",
    intermediate: "medium",
    advanced: "hard",
  };

  const course = useMemo(() => {
    if (!staticCourse) return null;

    // If courseMeta is available, merge it with static data
    if (courseMeta) {
      const result = {
        ...staticCourse,
        title: courseMeta.title ?? staticCourse.title,
        description: courseMeta.description ?? staticCourse.description,
        difficulty:
          levelToDifficulty[
            (courseMeta.level as string | undefined)?.toLowerCase() ?? ""
          ] ?? staticCourse.difficulty,
        duration: courseMeta.duration_hours
          ? `${courseMeta.duration_hours} hours`
          : staticCourse.duration,
      };
      return result;
    }

    // If no courseMeta, return static course as-is
    return staticCourse;
  }, [staticCourse, courseMeta]);

  // Load lesson completion progress for this course when user is logged in (only for enabled courses)
  useEffect(() => {
    if (!isCourseProgressEnabled) {
      setCompletedLessonIds([]);
      return;
    }

    if (!isEnrolled) {
      setCompletedLessonIds([]);
      return;
    }

    const accessToken = localStorage.getItem("accessToken");
    if (!slug) {
      setCompletedLessonIds([]);
      return;
    }

    const fetchProgress = async () => {
      try {
        if (!accessToken) {
          setCompletedLessonIds([]);
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
          navigate(`/auth?redirect=${encodeURIComponent(`/courses/${slug}`)}`);
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
      } catch {
        // best-effort; keep existing state on failure
      }
    };

    fetchProgress();
  }, [slug, isCourseProgressEnabled, isEnrolled, navigate]);

  // Get course-specific background image
  const courseBgImage = useMemo(() => {
    console.log('Getting background image for slug:', slug);
    console.log('Available backgrounds:', courseBackgrounds);
    console.log('Slug in backgrounds:', slug && courseBackgrounds[slug]);
    
    if (slug && courseBackgrounds[slug]) {
      console.log('Using mapped background:', courseBackgrounds[slug]);
      return courseBackgrounds[slug];
    }
    console.log('Using default background:', socFundamentalsBg);
    return socFundamentalsBg;
  }, [slug]);

  if (!slug) {
    return <Navigate to="/courses" replace />;
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-background">
        <Navbar />
        <div className="pt-20 flex items-center justify-center">
          <p className="text-muted-foreground">Loading course...</p>
        </div>
      </main>
    );
  }

  if (error || !course) {
    return (
      <main className="min-h-screen bg-background">
        <Navbar />
        <div className="pt-20 flex items-center justify-center">
          <p className="text-red-500">
            {error ?? "Course not found for this slug."}
          </p>
        </div>
      </main>
    );
  }

  const formatModuleId = (id: string) => id.replace(/^[a-z]+-/, "");

  const toggleModule = (moduleId: string) => {
    setOpenModules((prev) =>
      prev.includes(moduleId)
        ? prev.filter((id) => id !== moduleId)
        : [...prev, moduleId]
    );
  };

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

    if (slug === "network-fundamentals") {
      const nfQuizMap: Record<string, string> = {
        "nf-q1": "nf-q1",
        "nf-q2": "nf-q2",
        "nf-q3": "nf-q3",
        "nf-q4": "nf-q4",
        "nf-q5": "nf-q5",
        "nf-q6": "nf-q6",
        "nf-q7": "nf-q7",
        "nf-q8": "nf-q8",
        "nf-q9": "nf-q9",
        "nf-q10": "nf-q10",
      };
      return nfQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
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

    if (slug === "siem-fundamentals") {
      const siemQuizMap: Record<string, string> = {
        "1.5": "siem-q1",
        "2.5": "siem-q2",
        "3.5": "siem-q3",
        "4.5": "siem-q4",
        "5.5": "siem-q5",
        "6.5": "siem-q6",
      };
      return siemQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
    }

    if (slug === "incident-response-fundamentals") {
      const irQuizMap: Record<string, string> = {
        "1.5": "ir-q1",
        "2.5": "ir-q2",
        "3.5": "ir-q3",
        "4.5": "ir-q4",
        "5.5": "ir-q5",
        "6.5": "ir-q6",
      };
      return irQuizMap[lessonLikeQuizId] ?? lessonLikeQuizId;
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

  const getModuleGateQuizId = (module: any): string | null => {
    if (!module) return null;

    const lessons: any[] = Array.isArray(module.lessons) ? module.lessons : [];

    if (module.quizId && lessons.some((l) => l?.id === module.quizId)) {
      return module.quizId;
    }

    const quizLesson = lessons.find((l) => {
      if (!l?.id || !l?.title) return false;
      return String(l.title).toLowerCase().includes("quiz");
    });

    return quizLesson?.id ?? null;
  };

  // Function to determine if a lesson should be unlocked
  const isLessonUnlocked = (lesson: any, moduleIndex: number, lessonIndex: number) => {
    if (!isCourseProgressEnabled) {
      return true;
    }

    if (isLockedForPayment) {
      return false;
    }

    // For new users with no progress, use static data status
    if (effectiveCompletedLessonIds.length === 0) {
      return lesson.status === "unlocked" || lesson.status === "completed";
    }

    // If it's the first lesson of the first module, it's always unlocked
    if (moduleIndex === 0 && lessonIndex === 0) {
      return true;
    }

    // Check if it's a quiz lesson (title contains "quiz")
    const isQuiz = lesson.title.toLowerCase().includes('quiz');

    if (isQuiz) {
      // For quiz lessons, check if the previous lesson is completed
      const previousLessonIndex = lessonIndex - 1;
      if (previousLessonIndex >= 0) {
        const previousLesson = course.modules[moduleIndex].lessons[previousLessonIndex];
        return effectiveCompletedLessonIds.includes(previousLesson.id);
      }

      return false;
    }

    // For regular lessons after quiz, check if the quiz was passed with 70%
    if (lessonIndex > 0 && course.modules[moduleIndex].lessons[lessonIndex - 1]) {
      const previousLesson = course.modules[moduleIndex].lessons[lessonIndex - 1];
      const isPreviousQuiz = previousLesson.title.toLowerCase().includes('quiz');

      if (isPreviousQuiz) {
        // Check if quiz was passed with 70%
        const resolvedPrevQuizId = resolveQuizStorageId(previousLesson.id);
        const quizScore =
          effectiveQuizScores[resolvedPrevQuizId] ?? effectiveQuizScores[previousLesson.id];
        return quizScore !== undefined && quizScore >= 70;
      }
    }

    // For regular lessons, check if the previous lesson is completed
    if (lessonIndex > 0) {
      const previousLesson = course.modules[moduleIndex].lessons[lessonIndex - 1];
      return effectiveCompletedLessonIds.includes(previousLesson.id);
    }

    // For first lesson of subsequent modules, check if last lesson of previous module is completed
    if (moduleIndex > 0 && lessonIndex === 0) {
      const previousModule = course.modules[moduleIndex - 1];

      // If the previous module has an explicit quizId, require passing it (>= 70%)
      // before unlocking the next module.
      const gateQuizId = getModuleGateQuizId(previousModule);
      if (gateQuizId) {
        const storageGateQuizId = resolveQuizStorageId(gateQuizId);
        const prevQuizScore = effectiveQuizScores[storageGateQuizId] ?? effectiveQuizScores[gateQuizId];
        const passedPrevQuiz =
          (prevQuizScore != null && prevQuizScore >= 70) ||
          effectiveCompletedLessonIds.includes(storageGateQuizId) ||
          effectiveCompletedLessonIds.includes(gateQuizId);
        if (!passedPrevQuiz) return false;
      }

      const lastLesson = previousModule.lessons[previousModule.lessons.length - 1];
      return effectiveCompletedLessonIds.includes(lastLesson.id);
    }

    return false;
  };

  const totalLessons = course.modules.reduce(
    (acc, m) => acc + m.lessons.length,
    0
  );
  const completedLessons = course.modules.reduce(
    (acc, m) =>
      acc + m.lessons.filter((l) => effectiveCompletedLessonIds.includes(l.id)).length,
    0
  );
  const progressPercent = totalLessons > 0 ? Math.round((completedLessons / totalLessons) * 100) : 0;
  const isCourseCompleted = totalLessons > 0 && completedLessons >= totalLessons;

  const generateCertificatePngDataUrl = async (certName: string, certDate: string) => {
    try {
      if (!course) return null;

    const displayName = certName.trim() || "Student";
    // Add T12:00:00 to avoid off-by-one day from timezone conversion
    const issueDate = new Date(certDate + "T12:00:00").toLocaleDateString("en-GB", {
      day: "2-digit",
      month: "long",
      year: "numeric",
    });

      const img = new Image();
      img.crossOrigin = "anonymous";

      const imageSrc = certificateTemplatesBySlug[slug || ""] || "/certs/template11.jpg";

      await new Promise<void>((resolve, reject) => {
        img.onload = () => resolve();
        img.onerror = () => reject(new Error("Failed to load certificate template"));
        img.src = encodeURI(imageSrc);
      });

    if (document.fonts) {
      try {
        await document.fonts.load('600 48px "Montserrat"');
        await document.fonts.load('700 64px "Playfair Display"');
        await document.fonts.ready;
      } catch {
        // best-effort
      }
    }

    const canvas = document.createElement("canvas");
    canvas.width = img.naturalWidth || img.width;
    canvas.height = img.naturalHeight || img.height;

    const ctx = canvas.getContext("2d");
    if (!ctx) return null;

    ctx.textAlign = "left";
    ctx.textBaseline = "top";

    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    const w = canvas.width;
    const h = canvas.height;

    // Cover star at bottom-right (adjust size/position as needed)
    const starCoverSize = Math.max(w, h) * 0.0651;
    ctx.fillStyle = "#04162B";
    ctx.fillRect(w - starCoverSize, h - starCoverSize, starCoverSize, starCoverSize);

    const xLeft = Math.round(w * 0.075);

    // Student name (big, white)
    ctx.fillStyle = "#FFFFFF";
    ctx.font = `700 ${Math.round(h * 0.075)}px "Playfair Display", Georgia, serif`;
    wrapText(
      ctx,
      displayName,
      xLeft,
      Math.round(h * 0.395),
      Math.round(w * 0.55),
      Math.round(h * 0.085)
    );

    // Issue date
    ctx.fillStyle = "rgba(255,255,255,0.9)";
    ctx.font = `500 ${Math.round(h * 0.028)}px "Montserrat", Inter, Arial, sans-serif`;
    ctx.fillText(issueDate, xLeft, Math.round(h * 0.835));

    // QR Code (bottom right) - link to course page
    try {
      const courseUrl = `https://www.infosecdairies.io/courses/${slug}`;
      const qrDataUrl = await QRCode.toDataURL(courseUrl, {
        width: Math.round(Math.min(w, h) * 0.12),
        margin: 1,
        color: {
          dark: "#FFFFFF",
          light: "#04162B",
        },
      });
      const qrImg = new Image();
      await new Promise<void>((resolve, reject) => {
        qrImg.onload = () => resolve();
        qrImg.onerror = () => reject(new Error("Failed to load QR code"));
        qrImg.src = qrDataUrl;
      });
      const qrSize = Math.round(Math.min(w, h) * 0.12);
      const qrX = w - qrSize - Math.round(w * 0.05);
      const qrY = h - qrSize - Math.round(h * 0.05);
      ctx.drawImage(qrImg, qrX, qrY, qrSize, qrSize);
    } catch {
      // best-effort: skip QR if generation fails
    }

    const safeTitle = course.title.replace(/[^a-z0-9]+/gi, "-").replace(/(^-|-$)/g, "");
    const fileName = `${safeTitle}-certificate.png`;

      const dataUrl = canvas.toDataURL("image/png");

      return {
        dataUrl,
        fileName,
        displayName,
        issueDate,
      };
    } catch {
      return null;
    }
  };

  // Upload cert to backend (first time only). Returns upload data or null.
  const uploadCertIfNeeded = async (dataUrl: string): Promise<{cert_id?: string; issue_date?: string; student_name?: string; url?: string} | null> => {
    if (certMeta?.certId) return null; // already uploaded
    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken) return null;
    try {
      const res = await fetch(apiUrl("/api/certificates/upload/"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ image: dataUrl, course_slug: slug || "certificate" }),
      });
      if (!res.ok) return null;
      return await res.json();
    } catch {
      return null;
    }
  };

  const handleShareOnLinkedIn = async () => {
    if (!course || !user) return;

    if (serverCompleted === false) {
      setEnrollError("Please pass at least one quiz before sharing your certificate.");
      return;
    }

    // Use frozen server values — falls back to current user if certMeta not loaded yet
    const name = certMeta?.studentName || (user?.fullName || "Student");
    const date = certMeta?.issueDate || new Date().toISOString().slice(0, 10);

    const shareText = `I have completed my course on ${course.title} from BlueTeamers! 🎓\n\nhttps://www.infosecdairies.io/`;

    try {
      const cert = await generateCertificatePngDataUrl(name, date);
      if (!cert) return;

      const uploadData = await uploadCertIfNeeded(cert.dataUrl);

      if (uploadData?.cert_id) {
        setCertMeta(prev => prev ? {
          ...prev,
          exists: true,
          certId: uploadData.cert_id,
          studentName: uploadData.student_name || prev.studentName,
          issueDate: uploadData.issue_date || prev.issueDate,
        } : prev);
      }

      const imgUrl: string | undefined = uploadData?.url;
      if (!imgUrl) throw new Error("No image URL");

      const shareParams = new URLSearchParams({
        img: imgUrl,
        course: course.title,
        name: cert.displayName,
        date: cert.issueDate,
      });

      const sharePageUrl = apiUrl(`/api/certificates/share/?${shareParams.toString()}`);
      setShareModalText(shareText);
      setShareModalUrl(sharePageUrl);
      setShowShareModal(true);

    } catch {
      const fallbackSharePageUrl = "https://www.infosecdairies.io/share/certificate-completed.html";
      setShareModalText(shareText);
      setShareModalUrl(fallbackSharePageUrl);
      setShowShareModal(true);
    }
  };

  const handleDownloadCertificate = async () => {
    if (isCertDownloading) return;
    if (serverCompleted === false) {
      setEnrollError("Please pass at least one quiz before downloading your certificate.");
      return;
    }

    setIsCertDownloading(true);
    // Use frozen server values — falls back gracefully if certMeta not loaded yet
    const name = certMeta?.studentName || (user?.fullName || "Student");
    const date = certMeta?.issueDate || new Date().toISOString().slice(0, 10);

    try {
      const cert = await generateCertificatePngDataUrl(name, date);
      if (!cert) {
        setEnrollError("Could not generate certificate. Please try again.");
        return;
      }

      // Upload once (first time); subsequent downloads skip the upload
      const uploadData = await uploadCertIfNeeded(cert.dataUrl);
      if (uploadData?.cert_id) {
        setCertMeta(prev => prev ? {
          ...prev,
          exists: true,
          certId: uploadData.cert_id,
          studentName: uploadData.student_name || prev.studentName,
          issueDate: uploadData.issue_date || prev.issueDate,
        } : prev);
      }

      const a = document.createElement("a");
      a.href = cert.dataUrl;
      a.download = cert.fileName;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch {
      setEnrollError("Could not generate certificate. Please try again.");
    } finally {
      setIsCertDownloading(false);
    }
  };

  const handlePrimaryCta = async () => {
    if (!slug) return;

    // For coming-soon courses, do not hit backend; show friendly message instead
    if (!isCourseProgressEnabled) {
      setEnrollError("This course is under development. Content coming soon.");
      return;
    }

    const accessToken = localStorage.getItem("accessToken");
    if (!accessToken && !TESTING_MODE) {
      const returnUrl = slug === "network-fundamentals"
        ? `/courses/${slug}`
        : `/courses/${slug}/checkout`;
      navigate(`/auth?redirect=${encodeURIComponent(returnUrl)}`);
      return;
    }

    // If already enrolled, find and navigate to the next uncompleted lesson
    if (isEnrolled) {
      // Find the next uncompleted lesson
      let nextLesson = null;
      
      for (let moduleIndex = 0; moduleIndex < course.modules.length; moduleIndex++) {
        const module = course.modules[moduleIndex];
        for (let lessonIndex = 0; lessonIndex < module.lessons.length; lessonIndex++) {
          const lesson = module.lessons[lessonIndex];
          const resolvedQuizId = resolveQuizStorageId(lesson.id);
          const isCompleted =
            completedLessonIds.includes(lesson.id) ||
            completedLessonIds.includes(resolvedQuizId);

          const isUnlocked = isLessonUnlocked(lesson, moduleIndex, lessonIndex);
          
          // If this lesson is not completed and is unlocked, it's our next lesson
          if (!isCompleted && isUnlocked) {
            nextLesson = lesson;
            break;
          }
        }
        if (nextLesson) break;
      }
      
      // If all lessons are completed, allow review of first lesson
      if (!nextLesson) {
        // Course is completed - navigate to first lesson for review
        const firstModule = course.modules[0];
        const firstLesson = firstModule?.lessons?.[0];
        if (firstLesson) {
          const isQuiz = firstLesson.title.toLowerCase().includes('quiz');

          if (isQuiz && slug !== "blue-team-soc-fundamentals") {
            navigate(`/courses/${slug}/quiz/${firstLesson.id}`);
          } else {
            navigate(`/courses/${slug}/lesson/${firstLesson.id}`);
          }
        }
        return;
      }
      
      if (nextLesson) {
        console.log('Navigating to next lesson:', `/courses/${slug}/lesson/${nextLesson.id}`);
        console.log('Slug:', slug);
        console.log('Next lesson:', nextLesson);
        
        // Navigate to quiz page if it's a quiz
        const isQuiz = nextLesson.title.toLowerCase().includes('quiz');
        
        // For SOC Fundamentals, Continue Course should go to the lesson page
        // (quiz intro) even when the next lesson is a quiz like 1.5 or 2.5.
        if (isQuiz && slug !== "blue-team-soc-fundamentals") {
          navigate(`/courses/${slug}/quiz/${nextLesson.id}`);
        } else {
          navigate(`/courses/${slug}/lesson/${nextLesson.id}`);
        }
      }
      return;
    }

    // Free course: enroll directly
    if (slug === "network-fundamentals") {
      // Continue with existing enrollment flow for free course
    } else {
      // Paid course: redirect to checkout
      navigate(`/courses/${slug}/checkout`);
      return;
    }

    try {
      setEnrollLoading(true);
      setEnrollError(null);
      const res = await fetch(apiUrl(`/api/courses/${slug}/enroll/`), {
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
        navigate(`/auth?redirect=${encodeURIComponent(`/courses/${slug}`)}`);
        return;
      }

      const data = await res.json();
      if (!res.ok || data.status !== "enrolled") {
        setEnrollError("Could not enroll. Please try again.");
        return;
      }

      // Re-fetch the signed access token — this re-validates enrollment via backend
      recheckAccess();

      // After successful enrollment, immediately jump to the first lesson
      if (course && course.modules && course.modules.length > 0) {
        const firstModule = course.modules[0];
        const firstLesson = firstModule?.lessons?.[0];
        if (firstLesson) {
          const isQuiz = firstLesson.title.toLowerCase().includes('quiz');

          if (isQuiz) {
            navigate(`/courses/${slug}/quiz/${firstLesson.id}`);
          } else {
            navigate(`/courses/${slug}/lesson/${firstLesson.id}`);
          }
        }
      }
    } catch (err) {
      setEnrollError("Network error. Please try again.");
    } finally {
      setEnrollLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-background">
      <Navbar />

      {/* Hero Section with Course Background - confined to header area */}
      <div className="relative pt-20">
        {/* Course-specific Background - only for hero, subtle atmospheric */}
        <div className="absolute inset-0 h-[420px] overflow-hidden">
          <div
            className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-50"
            style={{
              backgroundImage: `url(${courseBgImage})`,
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-b from-background/70 via-background/85 to-background" />
          <div className="absolute inset-0 bg-gradient-to-r from-background/60 via-background/30 to-background/60" />
          {/* Extra dark overlay behind text area */}
          <div className="absolute inset-0 bg-background/40" />
        </div>

        <div className="container mx-auto px-4 relative z-10 py-8">
          <div className="max-w-6xl mx-auto">
            {/* Breadcrumb */}
            <Link
              to="/courses"
              className="inline-flex items-center gap-2 text-muted-foreground hover:text-primary transition-colors mb-8"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>Courses</span>
              <span className="text-muted-foreground/50">&gt;</span>
              <span className="text-foreground">{course.shortTitle}</span>
            </Link>

            {/* Header Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
              {/* Left - Course Info */}
              <div className="lg:col-span-2 space-y-6">
                {/* Title Row */}
                <div className="flex items-start gap-4">
                  <div className="w-14 h-14 rounded-xl bg-primary/15 border border-primary/25 flex items-center justify-center flex-shrink-0">
                    <BookOpen className="w-7 h-7 text-primary" />
                  </div>
                  <div>
                    <h1 className="text-3xl md:text-4xl font-bold text-foreground mb-3">
                      {course.title}
                    </h1>
                    <span className="inline-flex px-3 py-1 rounded-full text-xs font-medium bg-primary/15 text-primary border border-primary/25">
                      {difficultyLabels[course.difficulty]}
                    </span>
                  </div>
                </div>

                {/* Description */}
                <p className="text-muted-foreground text-lg leading-relaxed max-w-2xl">
                  {course.description}
                </p>

                {/* Outcomes */}
                <ul className="space-y-3">
                  <li className="flex items-start gap-3 text-muted-foreground">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
                    Understand the basics of SOC operations and cybersecurity
                    concepts.
                  </li>
                  <li className="flex items-start gap-3 text-muted-foreground">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
                    Analyze logs to identify suspicious activity and potential
                    threats.
                  </li>
                  <li className="flex items-start gap-3 text-muted-foreground">
                    <span className="w-1.5 h-1.5 rounded-full bg-primary mt-2 flex-shrink-0" />
                    Learn to use SIEM tools to monitor and respond to security
                    incidents.
                  </li>
                </ul>
              </div>

              {/* Right - Course Info Card */}
              <div className="lg:col-span-1">
                <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-6 shadow-lg shadow-black/20">
                  {/* Inner light reflection - top edge */}
                  <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />
                  {/* Inner light reflection - left edge */}
                  <div className="absolute inset-y-0 left-0 w-[1px] bg-gradient-to-b from-white/15 via-white/5 to-transparent" />
                  {/* Subtle inner teal glow */}
                  <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
                  {/* Left accent gradient line */}
                  <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

                  <div className="relative pl-3 space-y-4">
                    <h3 className="text-lg font-semibold text-foreground">
                      Course Info
                    </h3>

                    <div className="flex items-center gap-3">
                      <span className="text-muted-foreground">Difficulty:</span>
                      <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-card/50 border border-white/[0.08] text-foreground">
                        {difficultyLabels[course.difficulty]}
                      </span>
                    </div>

                    <div className="flex items-center gap-3">
                      <span className="text-muted-foreground">Duration:</span>
                      <span className="text-primary font-medium">
                        {course.duration}
                      </span>
                    </div>

                    <div className="flex items-center gap-2 text-muted-foreground">
                      <BookOpen className="w-4 h-4 text-primary" />
                      <span>Lessons, Quizzes, Labs</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content Section - Clean dark background */}
      <section className="relative bg-background pb-20">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-background to-background pointer-events-none" />

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-6xl mx-auto">
            {/* Tabs & Progress Section */}
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
              <div className="flex gap-2">
                <button
                  onClick={() => setActiveTab("modules")}
                  className={`px-5 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                    activeTab === "modules"
                      ? "bg-primary/15 text-primary border border-primary/25"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted/30"
                  }`}
                >
                  Modules
                </button>
                <button
                  onClick={() => setActiveTab("resources")}
                  className={`px-5 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                    activeTab === "resources"
                      ? "bg-primary/15 text-primary border border-primary/25"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted/30"
                  }`}
                >
                  Resources
                </button>
              </div>

              <div className="flex items-center gap-4">
                <span className="text-sm text-muted-foreground">
                  Progress:{" "}
                  <span className="text-foreground font-medium">
                    {completedLessons} / {totalLessons}
                  </span>{" "}
                  Lessons Completed
                </span>
                <div className="w-32">
                  <Progress value={progressPercent} className="h-2 bg-muted/30" />
                </div>
              </div>
            </div>

            {/* Modules + CTA Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Modules List */}
              <div className="lg:col-span-2 space-y-3">
                {activeTab === "modules" &&
                  course.modules.map((module, moduleIndex) => (
                    <Collapsible
                      key={module.id}
                      open={openModules.includes(module.id)}
                      onOpenChange={() => toggleModule(module.id)}
                    >
                      <div className="group relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] shadow-lg shadow-black/20 transition-all duration-500 ease-out hover:bg-card/35 hover:translate-y-[-2px] hover:border-white/[0.12] hover:shadow-xl hover:shadow-primary/10">
                        <div className="absolute -inset-[1px] rounded-xl bg-gradient-to-br from-primary/20 via-transparent to-secondary/10 opacity-0 group-hover:opacity-100 blur-sm transition-opacity duration-500 pointer-events-none" />
                        <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />
                        <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
                        <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50 group-hover:opacity-80 transition-opacity duration-500" />
                        <CollapsibleTrigger className="relative w-full px-6 py-4 pl-7 flex items-center justify-between hover:bg-white/[0.02] transition-colors">
                          <div className="flex items-center gap-3">
                            <span className="text-base font-semibold text-foreground">
                              {formatModuleId(module.id)}. {module.title}
                            </span>
                            {module.badge}
                          </div>
                          <ChevronDown
                            className={`w-5 h-5 text-muted-foreground transition-transform duration-200 ${
                              openModules.includes(module.id) ? "rotate-180" : ""
                            }`}
                          />
                        </CollapsibleTrigger>

                        <CollapsibleContent>
                          <div className="border-t border-white/[0.06]">
                            {module.lessons.map((lesson, lessonIndex) => {
                              const resolvedQuizId = resolveQuizStorageId(lesson.id);
                              const isCompleted =
                                effectiveCompletedLessonIds.includes(lesson.id) ||
                                effectiveCompletedLessonIds.includes(resolvedQuizId);
                              const isUnlocked = isLessonUnlocked(lesson, moduleIndex, lessonIndex);
                              const isLocked = !isCompleted && !isUnlocked;
                              const isQuiz = lesson.title.toLowerCase().includes('quiz');

                              return (
                                <div
                                  key={lesson.id}
                                  onClick={() => {
                                    if (isLocked) {
                                      if (isLockedForPayment) {
                                        window.alert("Please purchase/enroll to access this course.");
                                      } else {
                                        window.alert("Complete the module quiz (70%+) to unlock the next module.");
                                      }
                                      return;
                                    }

                                    if (isCourseProgressEnabled && !TESTING_MODE) {
                                      const accessToken = localStorage.getItem("accessToken");
                                      if (!accessToken) {
                                        // Show login prompt instead of auto-redirect
                                        setEnrollError("Please log in to access this lesson.");
                                        return;
                                      }
                                    }

                                    if (isCourseProgressEnabled && !isEnrolled) {
                                      handlePrimaryCta();
                                      return;
                                    }

                                    // Navigate to quiz page if it's a quiz
                                    if (isQuiz && slug !== "blue-team-soc-fundamentals") {
                                      navigate(`/courses/${slug}/quiz/${lesson.id}`);
                                    } else {
                                      navigate(`/courses/${slug}/lesson/${lesson.id}`);
                                    }
                                  }}
                                  className={`px-6 py-4 pl-7 flex items-center justify-between border-b border-white/[0.04] last:border-b-0 hover:bg-white/[0.02] transition-colors ${
                                    !isLocked ? "cursor-pointer" : ""
                                  } ${isQuiz && !isLocked ? "bg-orange-500/5 border-orange-500/20 hover:bg-orange-500/10" : ""}`}
                                >
                                  <div className="flex items-start gap-3">
                                    <span className="mt-0.5">
                                      {isCompleted ? (
                                        <CheckCircle className="w-4 h-4 text-primary" />
                                      ) : isLocked ? (
                                        <Lock className="w-4 h-4 text-muted-foreground/40" />
                                      ) : isQuiz ? (
                                        <FileQuestion className="w-4 h-4 text-primary" />
                                      ) : (
                                        <ChevronDown className="w-4 h-4 text-primary" />
                                      )}
                                    </span>
                                  <div>
                                    <div className="flex items-center gap-2">
                                      <span className="text-sm text-muted-foreground mr-2">
                                        {formatModuleId(lesson.id)}
                                      </span>
                                      <span
                                        className={`text-sm ${
                                          isLocked
                                            ? "text-muted-foreground/60"
                                            : "text-foreground"
                                        }`}
                                      >
                                        {lesson.title}
                                      </span>
                                    </div>
                                    {lesson.description && (
                                      <p className="text-xs text-muted-foreground/60 mt-1 max-w-lg">
                                        {lesson.description}
                                      </p>
                                    )}
                                  </div>
                                </div>

                                {isCompleted && !isQuiz && (
                                  <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-primary/15 text-primary border border-primary/25">
                                    Completed
                                  </span>
                                )}
                                {isLocked && (
                                  <span className="flex items-center gap-1.5 text-xs text-muted-foreground/50">
                                    <Lock className="w-3 h-3" />
                                    Locked
                                  </span>
                                )}
                                {isQuiz && !isCompleted && !isLocked && (
                                  <button
                                    onClick={(e) => {
                                      e.stopPropagation();
                                      navigate(`/courses/${slug}/quiz/${lesson.id}`);
                                    }}
                                    className="px-3 py-1.5 rounded-lg text-xs font-medium bg-orange-500 hover:bg-orange-600 text-white border border-orange-500/25 transition-colors"
                                  >
                                    Start Quiz
                                  </button>
                                )}
                                {isQuiz && isCompleted && (
                                  <div className="flex items-center gap-2">
                                    <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-green-500/15 text-green-400 border border-green-500/25">
                                      ✓ Completed
                                    </span>
                                    {effectiveQuizScores[resolvedQuizId] != null && (
                                      <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-primary/15 text-primary border border-primary/25">
                                        Score: {effectiveQuizScores[resolvedQuizId]}%
                                      </span>
                                    )}
                                    <button
                                      onClick={(e) => {
                                        e.stopPropagation();
                                        navigate(`/courses/${slug}/quiz/${lesson.id}`);
                                      }}
                                      className="px-3 py-1.5 rounded-lg text-xs font-medium bg-orange-500 hover:bg-orange-600 text-white border border-orange-500/25 transition-colors"
                                    >
                                      Retake
                                    </button>
                                  </div>
                                )}
                              </div>
                            );
                          })}
                          </div>
                        </CollapsibleContent>
                      </div>
                    </Collapsible>
                  ))}

                {activeTab === "resources" && (
                  <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-8 shadow-lg shadow-black/20">
                    <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
                    <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

                    <div className="relative pl-3">
                      <div className="flex items-center gap-3 mb-6">
                        <FolderOpen className="w-6 h-6 text-primary" />
                        <h3 className="text-lg font-semibold text-foreground">
                          Course Resources
                        </h3>
                        <span className="text-sm text-muted-foreground">
                          ({course.resources?.length || 0} resources)
                        </span>
                      </div>

                      {course.resources && course.resources.length > 0 ? (
                        <div className="grid gap-3">
                          <div className="space-y-3">
                            <h4 className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                              <Download className="w-4 h-4" />
                              Downloadable Materials
                            </h4>
                            {course.resources
                              .filter((r) => r.type !== "link")
                              .map((resource) => (
                                <div
                                  key={resource.id}
                                  role="button"
                                  tabIndex={0}
                                  onClick={() => {
                                    if (resource.url) {
                                      const a = document.createElement("a");
                                      a.href = resource.url;
                                      a.target = "_blank";
                                      a.rel = "noopener noreferrer";
                                      a.download = resource.url.split("/").pop() || `${resource.title}`;
                                      document.body.appendChild(a);
                                      a.click();
                                      a.remove();
                                      return;
                                    }

                                    navigate(`/courses/${course.id}/resource/${resource.id}`);
                                  }}
                                  onKeyDown={(e) => {
                                    if (e.key === "Enter" || e.key === " ") {
                                      e.preventDefault();
                                      (e.currentTarget as HTMLDivElement).click();
                                    }
                                  }}
                                  className="p-4 rounded-lg bg-card/30 border border-white/[0.06] flex items-center justify-between hover:bg-card/40 transition-colors group cursor-pointer"
                                >
                                  <div className="flex items-start gap-3">
                                    <div className="w-10 h-10 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center flex-shrink-0">
                                      {resource.type === "pdf" && (
                                        <FileText className="w-5 h-5 text-primary" />
                                      )}
                                      {resource.type === "cheatsheet" && (
                                        <FileText className="w-5 h-5 text-secondary" />
                                      )}
                                      {resource.type === "template" && (
                                        <FileText className="w-5 h-5 text-orange-400" />
                                      )}
                                      {resource.type === "tool" && (
                                        <FileText className="w-5 h-5 text-blue-400" />
                                      )}
                                    </div>
                                    <div>
                                      <span className="text-foreground font-medium">
                                        {resource.title}
                                      </span>
                                      <p className="text-xs text-muted-foreground mt-1">
                                        {resource.description}
                                      </p>
                                      <span className="inline-block mt-2 px-2 py-0.5 rounded text-xs bg-muted/30 text-muted-foreground capitalize">
                                        {resource.type}
                                      </span>
                                    </div>
                                  </div>
                                  <Download className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors" />
                                </div>
                              ))}
                          </div>

                          {course.resources.filter((r) => r.type === "link")
                            .length > 0 && (
                            <div className="space-y-3 mt-4">
                              <h4 className="text-sm font-medium text-muted-foreground flex items-center gap-2">
                                <ExternalLink className="w-4 h-4" />
                                Useful Links & Tools
                              </h4>
                              {course.resources
                                .filter((r) => r.type === "link")
                                .map((resource) => (
                                  <a
                                    key={resource.id}
                                    href={resource.url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="p-4 rounded-lg bg-card/30 border border-white/[0.06] flex items-center justify-between hover:bg-card/40 hover:border-primary/30 transition-colors group block"
                                  >
                                    <div className="flex items-start gap-3">
                                      <div className="w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center flex-shrink-0">
                                        <LinkIcon className="w-5 h-5 text-blue-400" />
                                      </div>
                                      <div>
                                        <span className="text-foreground font-medium group-hover:text-primary transition-colors">
                                          {resource.title}
                                        </span>
                                        <p className="text-xs text-muted-foreground mt-1">
                                          {resource.description}
                                        </p>
                                      </div>
                                    </div>
                                    <ExternalLink className="w-5 h-5 text-muted-foreground group-hover:text-primary transition-colors" />
                                  </a>
                                ))}
                            </div>
                          )}
                        </div>
                      ) : (
                        <div className="p-4 rounded-lg bg-card/30 border border-white/[0.06] text-center">
                          <p className="text-muted-foreground">
                            No resources available for this course yet.
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>

              {/* CTA Card */}
              <div className="lg:col-span-1">
                <div className="sticky top-28">
                  <div className="relative overflow-hidden rounded-xl bg-card/25 backdrop-blur-lg border border-white/[0.08] p-6 shadow-lg shadow-black/20">
                    <div className="absolute inset-x-0 top-0 h-[1px] bg-gradient-to-r from-transparent via-white/20 to-transparent" />
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-primary/[0.03] via-transparent to-secondary/[0.02] pointer-events-none" />
                    <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary to-secondary opacity-50" />

                    {enrollError && (
                      <p className={`mb-3 text-xs ${enrollError.includes('Congratulations') ? 'text-green-500' : 'text-red-500'}`}>{enrollError}</p>
                    )}

                    <button
                      onClick={handlePrimaryCta}
                      disabled={checkingEnrollment || enrollLoading}
                      className="relative w-full flex items-center justify-center gap-2 px-6 py-4 rounded-lg bg-primary/90 text-background font-semibold hover:bg-primary transition-colors group disabled:opacity-70 disabled:cursor-not-allowed"
                    >
                      <span>
                        {checkingEnrollment || enrollLoading
                          ? "Please wait..."
                          : isEnrolled && isCourseCompleted
                          ? "Review Course"
                          : isEnrolled
                          ? "Continue Course"
                          : slug === "network-fundamentals"
                          ? "Enroll"
                          : typeof displayPrice === "number"
                          ? `Buy Now (${symbol}${displayPrice})`
                          : "Buy Now"}
                      </span>
                      <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                    </button>

                    {isCourseCompleted && (
                      <div className="mt-3 space-y-2">
                        <button
                          onClick={handleDownloadCertificate}
                          disabled={isCertDownloading}
                          className="w-full px-6 py-3 rounded-lg text-sm font-semibold bg-primary/15 text-primary border border-primary/25 hover:bg-primary/20 transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
                        >
                          {isCertDownloading ? "Generating..." : "Download Certificate"}
                        </button>
                        <button
                          onClick={handleShareOnLinkedIn}
                          className="w-full px-6 py-3 rounded-lg text-sm font-semibold bg-blue-600/15 text-blue-400 border border-blue-600/25 hover:bg-blue-600/20 transition-colors"
                        >
                          Share on LinkedIn
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      {/* LinkedIn Share Modal */}
      {showShareModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4">
          <div className="bg-card border border-border rounded-xl max-w-md w-full p-6 shadow-2xl">
            <h3 className="text-lg font-semibold text-foreground mb-4">
              Share on LinkedIn
            </h3>
            <p className="text-sm text-muted-foreground mb-4">
              Copy this pre-written text and paste it in LinkedIn:
            </p>
            <textarea
              readOnly
              value={shareModalText}
              className="w-full h-32 p-3 rounded-lg bg-background border border-border text-foreground text-sm resize-none mb-4"
            />
            <div className="flex gap-3">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(shareModalText);
                  setCopied(true);
                  setTimeout(() => setCopied(false), 2000);
                }}
                className="flex-1 px-4 py-2 rounded-lg bg-primary text-primary-foreground font-medium hover:bg-primary/90 transition-colors"
              >
                {copied ? "Copied!" : "Copy Text"}
              </button>
              <button
                onClick={() => {
                  const linkedInUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareModalUrl)}`;
                  window.open(linkedInUrl, "_blank", "width=600,height=600");
                }}
                className="flex-1 px-4 py-2 rounded-lg bg-blue-600 text-white font-medium hover:bg-blue-700 transition-colors"
              >
                Open LinkedIn
              </button>
            </div>
            <button
              onClick={() => setShowShareModal(false)}
              className="w-full mt-3 px-4 py-2 rounded-lg text-muted-foreground hover:text-foreground transition-colors"
            >
              Close
            </button>
          </div>
        </div>
      )}

      </section>
    </main>
  );
};

export default CourseDetail;