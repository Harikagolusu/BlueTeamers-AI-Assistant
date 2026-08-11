import React from 'react';
import { Terminal, Shield, Zap, Search } from 'lucide-react';
import { ProfileCard, ProgressCard, EnrolledCoursesCard, RecommendationCard } from './PlatformCards';

interface EmptyStateDashboardProps {
  platformContext: any;
  onQuickPrompt: (prompt: string) => void;
}

export const EmptyStateDashboard: React.FC<EmptyStateDashboardProps> = ({ platformContext, onQuickPrompt }) => {
  // Only treat the dashboard as populated when there is REAL data: a named
  // profile, enrolled courses, or progress. A truthy-but-empty profile (e.g.
  // from an unauthenticated/invalid-token session) must not render placeholder
  // "Guest User" widgets.
  const hasRealProfile = !!(platformContext?.profile && (platformContext.profile.full_name || platformContext.profile.role));
  const hasPlatformData = !!platformContext && (
    hasRealProfile ||
    platformContext.courses?.length > 0 ||
    platformContext.progress?.length > 0
  );

  const SUGGESTED_PROMPTS = [
    { label: "Explain MITRE ATT&CK", icon: <Shield className="w-4 h-4" /> },
    { label: "Recommend SOC Courses", icon: <Zap className="w-4 h-4" /> },
    { label: "Analyze a Log Snippet", icon: <Terminal className="w-4 h-4" /> },
    { label: "Search CVE Database", icon: <Search className="w-4 h-4" /> }
  ];

  return (
    <div className="flex flex-col w-full h-full justify-center p-4 max-w-5xl mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
      
      {/* Header / Welcome */}
      <div className="text-center space-y-3 mb-4">
        <div className="inline-flex items-center justify-center p-3 rounded-2xl bg-primary/10 border border-primary/20 mb-2">
          <Terminal className="w-8 h-8 text-primary" />
        </div>
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-foreground">
          {platformContext?.profile?.full_name ? `Welcome back, ${platformContext.profile.full_name}` : "BlueTeamers AI Workspace"}
        </h1>
        <p className="text-muted-foreground max-w-lg mx-auto text-sm md:text-base">
          Your specialized cybersecurity intelligence assistant. Ask questions, analyze logs, or continue your training.
        </p>
      </div>

      {/* Dynamic Platform Dashboard */}
      {hasPlatformData && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full">
          {/* Profile takes 1 column on large screens */}
          {hasRealProfile && (
            <div className="col-span-1">
              <ProfileCard profile={platformContext.profile} />
            </div>
          )}

          {/* Progress / Enrollments */}
          {(platformContext.progress?.length > 0 || platformContext.courses?.length > 0) && (
            <div className="col-span-1 md:col-span-1 lg:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
              {platformContext.progress?.length > 0 ? (
                <ProgressCard progress={platformContext.progress} courses={platformContext.courses} />
              ) : null}
              {platformContext.courses?.length > 0 ? (
                <EnrolledCoursesCard courses={platformContext.courses} />
              ) : null}
            </div>
          )}

          {/* Recommendations span full width below if present */}
          {platformContext.recommendations?.length > 0 && (
            <div className="col-span-1 md:col-span-2 lg:col-span-3">
              <RecommendationCard recommendations={platformContext.recommendations} />
            </div>
          )}
        </div>
      )}

      {/* Quick Prompts */}
      <div className="pt-8 w-full max-w-3xl mx-auto">
        <h4 className="text-xs font-mono text-muted-foreground uppercase tracking-widest text-center mb-4">Quick Actions</h4>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {SUGGESTED_PROMPTS.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => onQuickPrompt(prompt.label)}
              className="flex items-center gap-3 p-3.5 rounded-xl border border-border/50 bg-muted/30 hover:bg-muted/80 hover:border-primary/30 transition-all text-left group"
            >
              <div className="p-2 rounded-lg bg-background border border-border group-hover:bg-primary/10 group-hover:border-primary/20 group-hover:text-primary transition-colors text-muted-foreground">
                {prompt.icon}
              </div>
              <span className="text-sm font-medium text-foreground/80 group-hover:text-foreground transition-colors">
                {prompt.label}
              </span>
            </button>
          ))}
        </div>
      </div>
      
    </div>
  );
};
