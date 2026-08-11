import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import Navbar from "@/components/Navbar";
import {
  BookOpen,
  Trophy,
  Clock,
  TrendingUp,
  CheckCircle,
  ChevronRight,
  Target,
  Calendar,
  Pencil,
  FileQuestion,
  Award,
} from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/context/AuthContext";
import { getCourseById } from "@/data/courses";
import { apiUrl } from "@/services/api";

interface ApiCourse {
  id: number;
  title: string;
  slug: string;
  level: string;
  duration_hours?: number | null;
}

interface EnrolledCourse {
  id: string;
  title: string;
  difficulty: string;
  completedLessons: number;
  totalLessons: number;
  progress: number;
  lastAccessed: string;
}

const recentActivity: {
  title: string;
  time: string;
  icon: typeof CheckCircle;
  color: string;
}[] = [];

interface ActivityItem {
  type: 'lesson' | 'quiz' | 'course_complete';
  title: string;
  courseTitle: string;
  timestamp: number;
}

const getRecentActivity = (userEmail: string): ActivityItem[] => {
  try {
    const userSpecificKey = `user_activity_log_${userEmail}`;
    const stored = localStorage.getItem(userSpecificKey);
    if (!stored) return [];
    const parsed = JSON.parse(stored) as ActivityItem[];
    return parsed
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, 5); // Get last 5 activities
  } catch {
    return [];
  }
};

export const logActivity = (type: ActivityItem['type'], title: string, courseTitle: string) => {
  try {
    // Get current user email from localStorage
    const userEmail = localStorage.getItem('userEmail');
    if (!userEmail) return; // Don't log activity if no user is logged in
    
    const existing = getRecentActivity(userEmail);
    const newActivity: ActivityItem = {
      type,
      title,
      courseTitle,
      timestamp: Date.now(),
    };
    // Remove duplicates (same type + title within last hour)
    const filtered = existing.filter(
      (a) =>
        !(a.type === type && a.title === title && Date.now() - a.timestamp < 3600000)
    );
    const updated = [newActivity, ...filtered].slice(0, 10);
    
    const userSpecificKey = `user_activity_log_${userEmail}`;
    localStorage.setItem(userSpecificKey, JSON.stringify(updated));
  } catch {
    // Silently fail
  }
};

const getDifficultyColor = (difficulty: string) => {
  switch (difficulty) {
    case "Easy": return "bg-blue-500/20 text-blue-400";
    case "Medium": return "bg-yellow-500/20 text-yellow-400";
    case "Hard": return "bg-red-500/20 text-red-400";
    default: return "bg-muted text-muted-foreground";
  }
};

const Dashboard = () => {
  const { user, login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [enrolledCourses, setEnrolledCourses] = useState<EnrolledCourse[]>([]);
  const [isEditingName, setIsEditingName] = useState(false);
  const [nameInput, setNameInput] = useState<string>(
    user?.fullName || user?.email?.split("@")[0] || "",
  );
  const [nameSaving, setNameSaving] = useState(false);
  const [nameError, setNameError] = useState<string | null>(null);

  const [recentActivity, setRecentActivity] = useState<ActivityItem[]>([]);

  const displayFirstName = (user?.fullName || "").trim().split(/\s+/)[0] || (user?.email ? user.email.split("@")[0] : "");

  useEffect(() => {
    if (!isAuthenticated) {
      navigate("/", { replace: true });
    }
  }, [isAuthenticated, navigate]);

  useEffect(() => {
    const fetchEnrollments = async () => {
      const accessToken = localStorage.getItem("accessToken");
      if (!accessToken) {
        return;
      }

      try {
        setLoading(true);
        setError(null);

        const coursesRes = await fetch(apiUrl(`/api/courses/`));
        if (!coursesRes.ok) {
          throw new Error("Failed to load courses");
        }
        const courses: ApiCourse[] = await coursesRes.json();

        const enrollmentChecks = await Promise.all(
          courses.map(async (course) => {
            const res = await fetch(
              apiUrl(`/api/courses/${course.slug}/enrollment/`),
              {
                headers: {
                  Authorization: `Bearer ${accessToken}`,
                },
              },
            );

            if (!res.ok) {
              return null;
            }
            const data = await res.json();
            if (data.status !== "enrolled") {
              return null;
            }

            const difficulty =
              course.level?.toLowerCase() === "advanced"
                ? "Hard"
                : course.level?.toLowerCase() === "intermediate"
                ? "Medium"
                : "Easy";

            // Map backend slug to static course id used in static course data
            let staticCourseId = course.slug;
            switch (course.slug) {
              case "blue-team-soc-fundamentals":
                staticCourseId = "soc-fundamentals";
                break;
              case "log-analysis-for-beginners":
                staticCourseId = "log-analysis";
                break;
              case "soc-analyst-practical-training":
                staticCourseId = "soc-analyst-practical";
                break;
              case "incident-response-fundamentals":
                staticCourseId = "incident-response";
                break;
              case "detection-engineering-basics":
                staticCourseId = "detection-engineering";
                break;
              case "malware-analysis-fundamentals":
                staticCourseId = "malware-analysis";
                break;
              case "threat-hunting-fundamentals":
                staticCourseId = "threat-hunting";
                break;
              case "network-security-monitoring":
                staticCourseId = "network-security-monitoring";
                break;
              case "network-fundamentals":
                staticCourseId = "network-fundamentals";
                break;
              case "soc-analyst-path":
                staticCourseId = "soc-analyst-path";
                break;
              default:
                // slugs that already match static ids (e.g. siem-fundamentals)
                staticCourseId = course.slug;
            }

            const staticCourse = getCourseById(staticCourseId);
            const totalLessons = staticCourse
              ? staticCourse.modules.reduce(
                  (sum, m) => sum + m.lessons.length,
                  0,
                )
              : 0;

            // Fetch backend lesson progress for this course
            let completedLessons = 0;
            let lastAccessedTime = Date.now();
            try {
              const progressRes = await fetch(
                apiUrl(`/api/courses/${course.slug}/progress/`),
                {
                  headers: {
                    Authorization: `Bearer ${accessToken}`,
                  },
                },
              );

              let completedIds: string[] = [];

              if (progressRes.ok) {
                const progressData: any[] = await progressRes.json();
                completedIds = progressData
                  .map((item) =>
                    item && item.lesson_id != null ? String(item.lesson_id) : null,
                  )
                  .filter((id: string | null): id is string => Boolean(id));
                
                // Track most recent completion time for "last accessed"
                const timestamps = progressData
                  .map((item) => item?.completed_at ? new Date(item.completed_at).getTime() : 0)
                  .filter((t: number) => t > 0);
                if (timestamps.length > 0) {
                  lastAccessedTime = Math.max(...timestamps);
                }
              }

              // Always merge with localStorage to ensure we don't lose progress
              const completedKey = `completed_lessons_${course.slug}`;
              const localIds = JSON.parse(localStorage.getItem(completedKey) || "[]") as string[];
              const merged = Array.from(new Set([...completedIds, ...localIds]));
              completedIds = merged;
              
              // Update localStorage with merged data
              localStorage.setItem(completedKey, JSON.stringify(completedIds));

              if (staticCourse) {
                const allLessonIds = staticCourse.modules.flatMap((m) =>
                  m.lessons.map((l) => l.id),
                );
                completedLessons = allLessonIds.filter((id) =>
                  completedIds.includes(id),
                ).length;
              } else {
                completedLessons = completedIds.length;
              }
            } catch {
              // Fallback to localStorage on error
              const completedKey = `completed_lessons_${course.slug}`;
              const localIds = JSON.parse(localStorage.getItem(completedKey) || "[]") as string[];
              if (staticCourse) {
                const allLessonIds = staticCourse.modules.flatMap((m) =>
                  m.lessons.map((l) => l.id),
                );
                completedLessons = allLessonIds.filter((id) =>
                  localIds.includes(id),
                ).length;
              } else {
                completedLessons = localIds.length;
              }
            }

            const formatLastAccessed = (timestamp: number): string => {
              const now = Date.now();
              const diff = now - timestamp;
              const minutes = Math.floor(diff / 60000);
              const hours = Math.floor(diff / 3600000);
              const days = Math.floor(diff / 86400000);
              
              if (minutes < 1) return 'just now';
              if (minutes < 60) return `${minutes}m ago`;
              if (hours < 24) return `${hours}h ago`;
              if (days < 7) return `${days}d ago`;
              return new Date(timestamp).toLocaleDateString();
            };

            const enrolled: EnrolledCourse = {
              id: course.slug,
              title: course.title,
              difficulty,
              completedLessons,
              totalLessons,
              progress: totalLessons ? Math.round((completedLessons / totalLessons) * 100) : 0,
              lastAccessed: formatLastAccessed(lastAccessedTime),
            };

            return enrolled;
          }),
        );

        setEnrolledCourses(enrollmentChecks.filter(Boolean) as EnrolledCourse[]);
        
        // Now that we have enrollment data, fetch recent activity
        if (user?.email) {
          const allActivities = getRecentActivity(user.email);
          const enrolledCourseSlugs = courses.map(c => c.slug);
          
          const filteredActivities = allActivities.filter(activity => 
            enrolledCourseSlugs.some(slug => activity.courseTitle.toLowerCase().includes(slug.toLowerCase())) ||
            activity.courseTitle.toLowerCase().includes('blue team') ||
            activity.courseTitle.toLowerCase().includes('log analysis') ||
            activity.courseTitle.toLowerCase().includes('threat hunting') ||
            activity.courseTitle.toLowerCase().includes('network security') ||
            activity.courseTitle.toLowerCase().includes('malware analysis') ||
            activity.courseTitle.toLowerCase().includes('detection engineering') ||
            activity.courseTitle.toLowerCase().includes('incident response') ||
            activity.courseTitle.toLowerCase().includes('network fundamentals')
          );
          
          setRecentActivity(filteredActivities);
        }
      } catch (err) {
        setError("Could not load your dashboard data. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchEnrollments();
  }, [user]);

  const enrolledCount = enrolledCourses.length;
  const completedLessonsCount = useMemo(
    () => enrolledCourses.reduce((sum, c) => sum + c.completedLessons, 0),
    [enrolledCourses],
  );
  const totalPoints = completedLessonsCount * 100; // simple placeholder formula
  const achievementsCount = useMemo(() => {
    // Count courses that are 100% complete as achievements/certifications
    return enrolledCourses.filter(
      (c) => c.totalLessons > 0 && c.completedLessons >= c.totalLessons,
    ).length;
  }, [enrolledCourses]);

  return (
    <main className="min-h-screen bg-background">
      <Navbar />
      
      <div className="pt-20 pb-16 px-4 md:px-8 max-w-7xl mx-auto">
        {/* Welcome Header */}
        <div className="mb-8 animate-fade-up">
          <h1 className="text-3xl md:text-4xl font-bold mb-2 flex flex-wrap items-center gap-3">
            <span>Welcome back,</span>
            {isEditingName ? (
              <div className="flex items-center gap-2">
                <input
                  className="bg-transparent border-b border-primary/60 focus:outline-none focus:border-primary text-2xl md:text-3xl font-bold text-primary px-1"
                  value={nameInput}
                  onChange={(e) => setNameInput(e.target.value)}
                  disabled={nameSaving}
                  autoFocus
                />
                <button
                  className="text-sm text-primary hover:text-primary/80"
                  onClick={async () => {
                    const trimmed = nameInput.trim();
                    if (!trimmed) {
                      setNameError("Name cannot be empty");
                      return;
                    }
                    if (/<|>/.test(trimmed)) {
                      setNameError("Name cannot contain < or > characters.");
                      return;
                    }

                    const accessToken = localStorage.getItem("accessToken");
                    if (!accessToken) {
                      setNameError("You must be logged in to change your name.");
                      return;
                    }

                    try {
                      setNameSaving(true);
                      setNameError(null);
                      const res = await fetch(apiUrl("/api/auth/profile/"), {
                        method: "PATCH",
                        headers: {
                          "Content-Type": "application/json",
                          Authorization: `Bearer ${accessToken}`,
                        },
                        body: JSON.stringify({ full_name: trimmed }),
                      });

                      if (!res.ok) {
                        try {
                          const errData = await res.json();
                          setNameError(errData.detail || "Could not update name. Please try again.");
                        } catch {
                          setNameError("Could not update name. Please try again.");
                        }
                        return;
                      }

                      const updatedUser = await res.json();
                      const refreshToken = localStorage.getItem("refreshToken") || undefined;
                      login({
                        email: updatedUser.email,
                        fullName: updatedUser.full_name,
                        tokens: { access: accessToken, refresh: refreshToken },
                      });
                      setIsEditingName(false);
                    } catch {
                      setNameError("Network error while updating name.");
                    } finally {
                      setNameSaving(false);
                    }
                  }}
                >
                  Save
                </button>
                <button
                  className="text-sm text-muted-foreground hover:text-foreground"
                  onClick={() => {
                    setIsEditingName(false);
                    setNameInput(
                      user?.fullName || user?.email?.split("@")[0] || "",
                    );
                    setNameError(null);
                  }}
                  disabled={nameSaving}
                >
                  Cancel
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <span className="gradient-text">
                  {displayFirstName || "Blue Teamer"}
                </span>
                <button
                  type="button"
                  className="p-1 rounded-full hover:bg-primary/10 text-primary"
                  onClick={() => setIsEditingName(true)}
                  aria-label="Edit username"
                >
                  <Pencil className="w-4 h-4" />
                </button>
              </div>
            )}
          </h1>
          {nameError && (
            <p className="text-sm text-red-500 mb-1">{nameError}</p>
          )}
          <p className="text-muted-foreground mb-1">
            Continue your blue team training journey
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 animate-fade-up" style={{ animationDelay: "100ms" }}>
          <div className="bg-card border border-border rounded-lg p-4 hover:border-primary/50 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-primary/10">
                <BookOpen className="w-5 h-5 text-primary" />
              </div>
              <span className="text-2xl font-bold">{enrolledCount}</span>
            </div>
            <p className="text-sm text-muted-foreground">Enrolled Courses</p>
          </div>
          
          <div className="bg-card border border-border rounded-lg p-4 hover:border-secondary/50 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-secondary/10">
                <CheckCircle className="w-5 h-5 text-secondary" />
              </div>
              <span className="text-2xl font-bold">{completedLessonsCount}</span>
            </div>
            <p className="text-sm text-muted-foreground">Lessons Completed</p>
          </div>
          
          <div className="bg-card border border-border rounded-lg p-4 hover:border-yellow-500/50 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-yellow-500/10">
                <Trophy className="w-5 h-5 text-yellow-400" />
              </div>
              <span className="text-2xl font-bold">{totalPoints}</span>
            </div>
            <p className="text-sm text-muted-foreground">Total Points</p>
          </div>
          
          <div className="bg-card border border-border rounded-lg p-4 hover:border-purple-500/50 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <div className="p-2 rounded-lg bg-purple-500/10">
                <Target className="w-5 h-5 text-purple-400" />
              </div>
              <span className="text-2xl font-bold">{achievementsCount}</span>
            </div>
            <p className="text-sm text-muted-foreground">Achievements</p>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Enrolled Courses */}
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between animate-fade-up" style={{ animationDelay: "200ms" }}>
              <h2 className="text-xl font-semibold flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-primary" />
                My Courses
              </h2>
              <Link to="/courses" className="text-sm text-primary hover:text-primary/80 transition-colors">
                Browse all courses
              </Link>
            </div>

            <div className="space-y-4">
              {loading && (
                <p className="text-sm text-muted-foreground">Loading your courses...</p>
              )}
              {error && !loading && (
                <p className="text-sm text-red-500">{error}</p>
              )}
              {!loading && !error && enrolledCourses.length === 0 && (
                <p className="text-sm text-muted-foreground">
                  You are not enrolled in any courses yet. Browse courses to get started.
                </p>
              )}
              {enrolledCourses.map((course, index) => (
                <div 
                  key={course.id}
                  className="bg-card/50 border border-border rounded-lg p-5 hover:border-primary/30 transition-all duration-300 group animate-fade-up"
                  style={{ animationDelay: `${250 + index * 50}ms` }}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <h3 className="font-semibold group-hover:text-primary transition-colors">
                          {course.title}
                        </h3>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${getDifficultyColor(course.difficulty)}`}>
                          {course.difficulty}
                        </span>
                      </div>
                      <p className="text-sm text-muted-foreground flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        Last accessed {course.lastAccessed}
                      </p>
                    </div>
                    <Link to={`/courses/${course.id}`}>
                      <Button size="sm" variant="outline" className="group-hover:border-primary group-hover:text-primary">
                        Continue
                        <ChevronRight className="w-4 h-4 ml-1" />
                      </Button>
                    </Link>
                  </div>
                  
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-muted-foreground">
                        {course.completedLessons} / {course.totalLessons} lessons
                      </span>
                      <span className="font-medium text-primary">{course.progress}%</span>
                    </div>
                    <Progress value={course.progress} className="h-2" />
                  </div>
                </div>
              ))}
            </div>

            {/* Achievements Section - placeholder for future backend data */}
          </div>

          {/* Sidebar - Recent Activity & Stats */}
          <div className="space-y-6">
            {/* User Rank Card */}
            <div className="bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20 rounded-lg p-5 animate-fade-up" style={{ animationDelay: "200ms" }}>
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-xl font-bold text-primary-foreground">
                  {(user?.fullName || user?.email || "U").charAt(0).toUpperCase()}
                </div>
                <div>
                  <p className="font-semibold">{displayFirstName || "Your account"}</p>
                  <p className="text-sm text-primary flex items-center gap-1">
                    <TrendingUp className="w-3 h-3" />
                    Blue Team Learner
                  </p>
                </div>
              </div>
              <div className="mt-4 pt-4 border-t border-border/50">
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Calendar className="w-4 h-4" />
                  Member since {new Date().toLocaleDateString('en-US', { month: 'short', year: 'numeric' })}
                </div>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-card border border-border rounded-lg p-5 animate-fade-up" style={{ animationDelay: "300ms" }}>
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Clock className="w-5 h-5 text-primary" />
                Recent Activity
              </h2>
              {recentActivity.length === 0 ? (
                <p className="text-sm text-muted-foreground">
                  No activity yet. Your recent lessons, quizzes, and achievements will show up here.
                </p>
              ) : (
                <div className="space-y-4">
                  {recentActivity.map((activity, index) => {
                    const getActivityIcon = (type: string) => {
                      switch (type) {
                        case 'lesson': return <BookOpen className="w-4 h-4 text-primary" />;
                        case 'quiz': return <FileQuestion className="w-4 h-4 text-orange-400" />;
                        case 'course_complete': return <Award className="w-4 h-4 text-yellow-400" />;
                        default: return <CheckCircle className="w-4 h-4 text-muted-foreground" />;
                      }
                    };
                    
                    const getActivityText = (type: string) => {
                      switch (type) {
                        case 'lesson': return 'Completed lesson';
                        case 'quiz': return 'Completed quiz';
                        case 'course_complete': return 'Completed course';
                        default: return 'Activity';
                      }
                    };

                    const formatTime = (timestamp: number) => {
                      const diff = Date.now() - timestamp;
                      const minutes = Math.floor(diff / 60000);
                      const hours = Math.floor(diff / 3600000);
                      const days = Math.floor(diff / 86400000);
                      
                      if (minutes < 1) return 'just now';
                      if (minutes < 60) return `${minutes}m ago`;
                      if (hours < 24) return `${hours}h ago`;
                      if (days < 7) return `${days}d ago`;
                      return new Date(timestamp).toLocaleDateString();
                    };
                    
                    return (
                      <div key={index} className="flex items-start gap-3">
                        <div className="mt-0.5">
                          {getActivityIcon(activity.type)}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm truncate">
                            {getActivityText(activity.type)}: <span className="font-medium">{activity.title}</span>
                          </p>
                          <p className="text-xs text-muted-foreground">
                            {activity.courseTitle} · {formatTime(activity.timestamp)}
                          </p>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Quick Actions */}
            <div className="bg-card border border-border rounded-lg p-5 animate-fade-up" style={{ animationDelay: "400ms" }}>
              <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
              <div className="space-y-2">
                <Link to="/courses" className="block">
                  <Button variant="outline" className="w-full justify-start">
                    <BookOpen className="w-4 h-4 mr-2" />
                    Browse Courses
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Dashboard;
