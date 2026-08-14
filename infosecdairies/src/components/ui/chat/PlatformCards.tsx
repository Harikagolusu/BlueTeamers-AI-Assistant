import React from 'react';
import { Link } from 'react-router-dom';
import { User, BookOpen, GraduationCap, Compass, ExternalLink, Info, Clock, BarChart3, PlayCircle, Star, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { safeUrl } from '@/lib/safeUrl';
import { getCourseBySlug } from '@/data/courses';

// Import all course thumbnails (keyed by canonical course slug, matching the
// URL slugs the backend emits in course_sources metadata).
import socCourseBg from "@/assets/soc-course-bg.jpg";
import logAnalysisBg from "@/assets/courses/log-analysis-bg.jpg";
import siemFundamentalsBg from "@/assets/courses/siem-fundamentals-bg.jpg";
import socAnalystPracticalBg from "@/assets/courses/soc-analyst-practical-bg.jpg";
import incidentResponseBg from "@/assets/courses/incident-response-bg.jpg";
import threatHuntingBg from "@/assets/courses/threat-hunting-bg.jpg";
import detectionEngineeringBg from "@/assets/courses/detection-engineering-bg.jpg";
import malwareAnalysisBg from "@/assets/courses/malware-analysis-bg.jpg";
import networkFundamentalsBg from "@/assets/courses/network-fundamentals-bg.jpg";

const courseBackgrounds: Record<string, string> = {
  "blue-team-soc-fundamentals": socCourseBg,
  "log-analysis-for-beginners": logAnalysisBg,
  "siem-fundamentals": siemFundamentalsBg,
  "soc-analyst-practical-training": socAnalystPracticalBg,
  "incident-response-fundamentals": incidentResponseBg,
  "threat-hunting-fundamentals": threatHuntingBg,
  "detection-engineering-basics": detectionEngineeringBg,
  "malware-analysis-fundamentals": malwareAnalysisBg,
  "network-fundamentals": networkFundamentalsBg,
};

export const ProfileCard: React.FC<{ profile: any }> = ({ profile }) => {
  if (!profile) return null;
  
  return (
    <div className="p-5 rounded-xl border border-primary/20 bg-zinc-950/80 shadow-[0_0_20px_rgba(0,186,216,0.05)] text-center relative overflow-hidden group">
      <div className="absolute inset-0 circuit-pattern opacity-[0.03] group-hover:opacity-[0.05] transition-opacity"></div>
      <div className="w-14 h-14 mx-auto mb-3 rounded-full bg-primary/10 flex items-center justify-center border border-primary/30 text-primary relative z-10">
        <User className="w-7 h-7" />
      </div>
      <h4 className="font-semibold text-lg text-primary relative z-10 tracking-wide">
        {profile.full_name || "Guest User"}
      </h4>
      <p className="text-xs text-muted-foreground mt-1 font-mono uppercase tracking-widest relative z-10">
        {profile.role || "SOC Analyst"}
      </p>
    </div>
  );
};

export const ProgressCard: React.FC<{ progress: any[]; courses: any[] }> = ({ progress, courses }) => {
  if (!progress || progress.length === 0) return null;

  return (
    <div className="p-5 rounded-xl border border-primary/20 bg-zinc-950/80 shadow-[0_0_20px_rgba(0,186,216,0.05)] h-full">
      <div className="flex items-center gap-2 mb-4">
        <GraduationCap className="w-4 h-4 text-primary" />
        <h4 className="text-xs font-mono text-muted-foreground uppercase tracking-widest">Active Progress</h4>
      </div>
      
      <div className="space-y-4">
        {progress.map((prog, idx) => {
          const course = courses?.find(c => c.slug === prog.course_slug || c.id === prog.course_slug);
          return (
            <div key={idx} className="group">
              <div className="flex justify-between items-center mb-1.5">
                <span className="font-medium text-foreground text-sm truncate pr-2">
                  {course?.title || prog.course_slug}
                </span>
                <span className="text-xs text-emerald-400 font-mono font-medium">
                  {prog.percent_complete}%
                </span>
              </div>
              <div className="w-full bg-zinc-900/80 border border-zinc-800 rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-emerald-500 h-full rounded-full transition-all duration-1000 ease-out group-hover:shadow-[0_0_10px_rgba(16,185,129,0.5)]" 
                  style={{ width: `${prog.percent_complete}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export const EnrolledCoursesCard: React.FC<{ courses: any[] }> = ({ courses }) => {
  if (!courses || courses.length === 0) return null;

  return (
    <div className="p-5 rounded-xl border border-primary/20 bg-zinc-950/80 shadow-[0_0_20px_rgba(0,186,216,0.05)] h-full">
      <div className="flex items-center gap-2 mb-4">
        <BookOpen className="w-4 h-4 text-primary" />
        <h4 className="text-xs font-mono text-muted-foreground uppercase tracking-widest">Enrolled Courses</h4>
      </div>
      
      <div className="flex flex-col gap-2 text-sm">
        {courses.map((c, idx) => (
          <div key={idx} className="flex items-start gap-3 p-2.5 rounded-lg bg-zinc-900/50 border border-zinc-800/50 hover:bg-zinc-800/50 hover:border-primary/30 transition-all cursor-default">
            <div className="w-1.5 h-1.5 rounded-full bg-primary/60 mt-1.5 shrink-0 shadow-[0_0_5px_rgba(0,186,216,0.5)]"></div>
            <div className="flex-1 min-w-0">
              <p className="text-foreground font-medium truncate">{c.title}</p>
              {c.level && <p className="text-[10px] text-muted-foreground uppercase mt-0.5 font-mono">{c.level}</p>}
            </div>
            <button
              onClick={() => window.open(`/courses/${c.slug || c.id}`, "_blank")}
              className="text-muted-foreground hover:text-primary transition-colors p-1"
              title="Open Course"
            >
              <ExternalLink className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export const CourseCard: React.FC<{ card: any }> = ({ card }) => {
  const [showInfo, setShowInfo] = React.useState(false);
  const actions = card.actions && card.actions.length > 0 ? card.actions : (card.action ? [card.action] : []);
  const progress = card.progress && /^\d+$/.test(String(card.progress).replace('%', '')) ? parseInt(String(card.progress).replace('%', ''), 10) : null;

  const handleAction = (action: any) => {
    const url = action?.payload?.url;
    if (action?.action_type === 'course_info') {
      setShowInfo(prev => !prev);
      return;
    }
    if (url) {
      // Only ever open a URL that survives the scheme whitelist — the payload
      // originates from an AI response, so javascript:/data: must be impossible.
      window.open(safeUrl(url), '_blank');
    }
  };

  return (
    <div className="p-5 rounded-xl border border-primary/20 bg-zinc-950/80 shadow-[0_0_20px_rgba(0,186,216,0.05)] flex flex-col gap-3 relative overflow-hidden h-full">
      <div className="flex items-start justify-between gap-2">
        <h4 className="font-medium text-foreground text-sm leading-snug">{card.title}</h4>
        {(card.difficulty || card.duration) && (
          <span className="text-[9px] text-muted-foreground uppercase font-mono shrink-0 pt-0.5">
            {card.difficulty}{card.duration ? ` • ${card.duration}` : ''}
          </span>
        )}
      </div>

      {progress !== null && (
        <div className="flex items-center gap-2">
          <div className="flex-1 bg-zinc-900/80 border border-zinc-800 rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-emerald-500 h-full rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${Math.min(100, progress)}%` }}
            ></div>
          </div>
          <span className="text-[10px] text-emerald-400 font-mono shrink-0">{card.progress}</span>
        </div>
      )}

      {showInfo && card.description && (
        <p className="text-xs text-muted-foreground leading-relaxed border-t border-zinc-800 pt-2.5">{card.description}</p>
      )}

      <div className="flex flex-wrap gap-2 mt-auto pt-1">
        {actions.map((a: any, aIdx: number) => (
          <Button
            key={aIdx}
            size="sm"
            variant={a.action_type === 'enroll_course' ? 'default' : 'outline'}
            onClick={() => handleAction(a)}
            className="h-8 text-xs gap-1.5"
          >
            {a.action_type === 'course_info' ? <Info className="w-3 h-3" /> : null}
            {a.label}
          </Button>
        ))}
      </div>
    </div>
  );
};

export const RecommendationCard: React.FC<{ recommendations: any[] }> = ({ recommendations }) => {  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="p-5 rounded-xl border border-emerald-500/20 bg-emerald-950/10 shadow-[0_0_20px_rgba(16,185,129,0.05)] relative overflow-hidden h-full">
      <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none"></div>
      
      <div className="flex items-center gap-2 mb-4 relative z-10">
        <Compass className="w-4 h-4 text-emerald-400" />
        <h4 className="text-xs font-mono text-emerald-400/80 uppercase tracking-widest">Recommended Actions</h4>
      </div>

      <div className="flex flex-col gap-3 relative z-10">
        {recommendations.map((rec, idx) => (
          <div key={idx} className="p-3.5 rounded-lg bg-zinc-950/60 border border-emerald-500/20 hover:border-emerald-500/50 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-3 group">
            <div className="flex-1">
              <div className="font-medium text-emerald-400 text-sm group-hover:text-emerald-300 transition-colors">{rec.title}</div>
              <p className="text-xs text-muted-foreground mt-1 line-clamp-1">{rec.reason}</p>
            </div>
            <Button 
              className="w-full sm:w-auto shrink-0 bg-emerald-500/10 hover:bg-emerald-500 hover:text-white border border-emerald-500/30 transition-all text-xs h-8 text-emerald-400"
              onClick={() => window.open(`/courses/${rec.item_id}`, "_blank")}
            >
              Launch Module
            </Button>
          </div>
        ))}
      </div>
    </div>
  );
};

export const CourseSourceCard: React.FC<{ source: any }> = ({ source }) => {
  if (!source) return null;

  const course = getCourseBySlug(source.course_slug);
  const lessons = (source.lessons && source.lessons.length > 0)
    ? source.lessons
    : (source.lesson ? [{ id: source.lesson_id, title: source.lesson }] : []);
  const lessonsCount = source.lessons_count ?? lessons.length;
  const thumbnail = source.thumbnail || courseBackgrounds[source.course_slug];
  const duration = lessons[0]?.duration || course?.modules?.flatMap((m: any) => m.lessons || []).find((l: any) => l.id === lessons[0]?.id)?.duration || source.duration || "N/A";
  const level = source.level || course?.difficulty || "Beginner";
  const progress =
    typeof source.progress === 'number' && source.progress >= 0
      ? Math.min(100, Math.round(source.progress))
      : null;
  const rating = source.rating
    ? Math.max(0, Math.min(5, Math.round(source.rating)))
    : null;

  const lessonUrl = source.action?.url || (source.course_slug && lessons[0]?.id ? `/courses/${source.course_slug}/lesson/${lessons[0].id}` : "#");
  const courseUrl = source.course_action?.url || (source.course_slug ? `/courses/${source.course_slug}` : "#");

  return (
    <div className="p-4 rounded-xl border border-primary/20 bg-zinc-950/80 shadow-[0_0_20px_rgba(0,186,216,0.05)] flex flex-col gap-3 relative overflow-hidden group transition-all duration-300 hover:border-primary/40">
      <div className="flex gap-3">
        {thumbnail ? (
          <img src={thumbnail} alt={source.title} className="w-16 h-16 sm:w-20 sm:h-20 rounded-lg object-cover border border-zinc-800 shrink-0" />
        ) : (
          <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-lg bg-gradient-to-br from-primary/20 to-emerald-500/10 border border-primary/20 flex items-center justify-center shrink-0">
            <BookOpen className="w-6 h-6 text-primary" />
          </div>
        )}
        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-2">
            <p className="text-[10px] font-mono text-primary uppercase tracking-widest shrink-0">Course Source</p>
            {source.label && (
              <span className="text-[9px] font-mono px-1.5 py-0.5 rounded-full bg-primary/10 border border-primary/25 text-primary uppercase tracking-wider shrink-0">
                {source.label}
              </span>
            )}
          </div>
          <h4 className="font-semibold text-sm text-foreground leading-snug mt-0.5 truncate">{source.title}</h4>
          <p className="flex flex-wrap items-center gap-x-2 gap-y-0.5 text-[10px] font-mono text-muted-foreground mt-1">
            <span className="flex items-center gap-1"><BarChart3 className="w-3 h-3 text-primary/70" />{level}</span>
            <span className="flex items-center gap-1"><Clock className="w-3 h-3 text-primary/70" />{duration}</span>
            {rating !== null && (
              <span className="flex items-center gap-0.5">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Star key={i} className={`w-3 h-3 ${i < rating ? "text-yellow-400 fill-yellow-400" : "text-zinc-700"}`} />
                ))}
              </span>
            )}
          </p>
        </div>
      </div>

      {source.description && (
        <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
          {source.description}
        </p>
      )}

      {progress !== null && (
        <div className="flex items-center gap-2">
          <div className="flex-1 bg-zinc-900/80 border border-zinc-800 rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-emerald-500 h-full rounded-full transition-all duration-1000 ease-out group-hover:shadow-[0_0_10px_rgba(16,185,129,0.5)]"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <span className="text-[10px] text-emerald-400 font-mono shrink-0">{progress}%</span>
        </div>
      )}

      {lessons.length > 0 && (
        <div className="flex flex-col gap-1.5">
          <p className="text-[10px] font-mono text-muted-foreground uppercase tracking-widest">
            Referenced {lessonsCount > 1 ? `Lessons (${lessonsCount})` : "Lesson"}
          </p>
          {lessons.slice(0, 5).map((l: any) => (
            <div key={l.id} className="flex items-start gap-2">
              <span className="w-3.5 h-3.5 rounded-sm bg-emerald-500/10 border border-emerald-500/40 text-emerald-400 flex items-center justify-center mt-0.5 shrink-0">
                <Check className="w-2.5 h-2.5" />
              </span>
              <div className="min-w-0">
                <span className="text-xs text-foreground truncate block">{l.title}</span>
                {l.module && <span className="text-[9px] text-muted-foreground/70 font-mono block truncate">{l.module}</span>}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="flex flex-wrap gap-2 mt-auto pt-1">
        <Link to={lessonUrl}>
          <Button size="sm" className="h-8 text-xs gap-1.5">
            <PlayCircle className="w-3.5 h-3.5" />
            {source.action?.label || "Continue Learning"}
          </Button>
        </Link>
        <Link to={courseUrl}>
          <Button size="sm" variant="outline" className="h-8 text-xs gap-1.5">
            <BookOpen className="w-3.5 h-3.5" />
            {source.course_action?.label || "View Course"}
          </Button>
        </Link>
      </div>
    </div>
  );
};

export const SuggestedCourseCard: React.FC<{ suggestion: any }> = ({ suggestion }) => {
  if (!suggestion) return null;

  const enrolled = !!suggestion.enrolled;
  const continueUrl = enrolled
    ? (suggestion.lesson_url || suggestion.course_url || (suggestion.course_slug ? `/courses/${suggestion.course_slug}` : "#"))
    : "#";
  const courseUrl = suggestion.course_url || (suggestion.course_slug ? `/courses/${suggestion.course_slug}` : "#");
  const enrollUrl = suggestion.enroll_url || (suggestion.course_slug ? `/courses/${suggestion.course_slug}/checkout` : "#");
  const thumbnail = suggestion.thumbnail || courseBackgrounds[suggestion.course_slug];
  const progress =
    typeof suggestion.progress === 'number' && suggestion.progress >= 0
      ? Math.min(100, Math.round(suggestion.progress))
      : null;

  return (
    <div className="p-4 rounded-xl border border-primary/20 bg-zinc-950/80 shadow-[0_0_20px_rgba(0,186,216,0.05)] flex flex-col gap-3 relative overflow-hidden group transition-all duration-300 hover:border-primary/40">
      <div className="flex gap-3">
        {thumbnail ? (
          <img src={thumbnail} alt={suggestion.title} className="w-16 h-16 sm:w-20 sm:h-20 rounded-lg object-cover border border-zinc-800 shrink-0" />
        ) : (
          <div className="w-16 h-16 sm:w-20 sm:h-20 rounded-lg bg-gradient-to-br from-primary/20 to-emerald-500/10 border border-primary/20 flex items-center justify-center shrink-0">
            <BookOpen className="w-6 h-6 text-primary" />
          </div>
        )}
        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-2">
            <h4 className="font-semibold text-sm text-foreground leading-snug truncate">{suggestion.title}</h4>
            {enrolled && (
              <span className="flex items-center gap-1 text-[10px] font-mono text-emerald-400 shrink-0">
                <Check className="w-3 h-3" />Enrolled
              </span>
            )}
          </div>
          <p className="flex flex-wrap items-center gap-x-2 gap-y-0.5 text-[10px] font-mono text-muted-foreground mt-1">
            <span className="flex items-center gap-1"><BarChart3 className="w-3 h-3 text-primary/70" />{suggestion.level || "Beginner"}</span>
            <span className="flex items-center gap-1"><Clock className="w-3 h-3 text-primary/70" />{suggestion.duration || "N/A"}</span>
          </p>
        </div>
      </div>

      {suggestion.description && (
        <p className="text-xs text-muted-foreground leading-relaxed line-clamp-3">
          {suggestion.description}
        </p>
      )}

      {enrolled && progress !== null && (
        <div className="flex items-center gap-2">
          <div className="flex-1 bg-zinc-900/80 border border-zinc-800 rounded-full h-1.5 overflow-hidden">
            <div
              className="bg-emerald-500 h-full rounded-full transition-all duration-1000 ease-out group-hover:shadow-[0_0_10px_rgba(16,185,129,0.5)]"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <span className="text-[10px] text-emerald-400 font-mono shrink-0">{progress}%</span>
        </div>
      )}

      <div className="mt-auto pt-1 flex flex-wrap gap-2">
        {enrolled ? (
          <>
            <Link to={continueUrl} className="flex-1 sm:flex-none">
              <Button size="sm" className="h-8 text-xs gap-1.5 w-full">
                <PlayCircle className="w-3.5 h-3.5" />
                Continue Course
              </Button>
            </Link>
            <Link to={courseUrl} className="flex-1 sm:flex-none">
              <Button size="sm" variant="outline" className="h-8 text-xs gap-1.5 w-full">
                <BookOpen className="w-3.5 h-3.5" />
                View Course
              </Button>
            </Link>
          </>
        ) : (
          <>
            <Link to={courseUrl} className="flex-1 sm:flex-none">
              <Button size="sm" variant="outline" className="h-8 text-xs gap-1.5 w-full">
                <BookOpen className="w-3.5 h-3.5" />
                View Course
              </Button>
            </Link>
            <Link to={enrollUrl} className="flex-1 sm:flex-none">
              <Button size="sm" className="h-8 text-xs gap-1.5 w-full">
                <ExternalLink className="w-3.5 h-3.5" />
                Enroll Course
              </Button>
            </Link>
          </>
        )}
      </div>
    </div>
  );
};
