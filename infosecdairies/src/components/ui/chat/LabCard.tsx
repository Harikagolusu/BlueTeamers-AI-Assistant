import React, { useState } from 'react';
import {
  FlaskConical,
  CheckCircle2,
  XCircle,
  Circle,
  Lightbulb,
  Send,
  RefreshCw,
  Activity,
  Shield,
  Mail,
} from 'lucide-react';
import { Button } from '@/components/ui/button';

const DIFFICULTY_TONE: Record<string, string> = {
  beginner: 'text-emerald-400 border-emerald-500/30',
  intermediate: 'text-amber-400 border-amber-500/30',
  advanced: 'text-rose-400 border-rose-500/30',
};

const ICONS: Record<string, React.ElementType> = {
  mail: Mail,
  activity: Activity,
  shield: Shield,
};

export const LabCard: React.FC<{
  lab: any;
  disabled?: boolean;
  onAnswer: (answer: string) => void;
  onHint: () => void;
  onRestart: () => void;
}> = ({ lab, disabled, onAnswer, onHint, onRestart }) => {
  const [draft, setDraft] = useState('');
  if (!lab || !lab.active) return null;

  const Icon = ICONS[lab.icon] || FlaskConical;
  const completed = !!lab.completed;
  const steps: Array<{ step_id: string; title: string; completed: boolean; current: boolean }> =
    Array.isArray(lab.steps) ? lab.steps : [];

  const submit = () => {
    const text = draft.trim();
    if (!text || disabled) return;
    onAnswer(text);
    setDraft('');
  };

  return (
    <div className="mt-2 w-full max-w-[560px] not-prose rounded-2xl border border-primary/25 bg-gradient-to-b from-zinc-900/95 to-zinc-950/95 shadow-[0_0_25px_rgba(0,186,216,0.08)] overflow-hidden">
      {/* Header */}
      <div className="px-4 py-3 border-b border-primary/15 bg-primary/[0.06] flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="w-7 h-7 rounded-lg bg-primary/15 border border-primary/30 flex items-center justify-center">
            <Icon className="w-4 h-4 text-primary" />
          </span>
          <div>
            <p className="text-xs font-mono uppercase tracking-widest text-primary">Practice Lab</p>
            <p className="text-[10px] text-muted-foreground font-mono">
              {lab.title} — {completed ? 'Complete' : `Step ${lab.current_step} of ${lab.total}`}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {lab.difficulty && (
            <span className={`text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded-md border bg-zinc-950/60 ${DIFFICULTY_TONE[lab.difficulty] || 'text-muted-foreground border-border/60'}`}>
              {lab.difficulty}
            </span>
          )}
          {lab.category && (
            <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground px-2 py-0.5 rounded-md border border-border/60 bg-zinc-950/60">
              {lab.category}
            </span>
          )}
        </div>
      </div>

      {/* Stepper */}
      {steps.length > 0 && (
        <div className="px-4 pt-4">
          <div className="flex items-center gap-2 flex-wrap">
            {steps.map((s, i) => (
              <div key={s.step_id} className="flex items-center gap-2">
                <div
                  className={`flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[10px] font-mono ${
                    s.completed
                      ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-400'
                      : s.current
                        ? 'border-primary/50 bg-primary/10 text-primary'
                        : 'border-zinc-700/60 bg-zinc-900/40 text-zinc-500'
                  }`}
                >
                  {s.completed ? <CheckCircle2 className="w-3 h-3" /> : <Circle className="w-3 h-3" />}
                  <span className="max-w-[110px] truncate">{s.title}</span>
                </div>
                {i < steps.length - 1 && <div className="w-2 h-px bg-zinc-700/70" />}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Body */}
      <div className="px-4 py-4">
        {completed ? (
          <div className="space-y-3">
            <div className="rounded-xl border border-emerald-500/25 bg-emerald-500/[0.06] px-3 py-2.5 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <p className="text-sm text-zinc-200">
                Lab complete — you answered <span className="text-emerald-400 font-semibold">{lab.score} / {lab.total}</span> correctly.
              </p>
            </div>

            {/* Per-step review below the summary */}
            {Array.isArray(lab.review) && lab.review.length > 0 && (
              <div className="pt-2">
                <p className="flex items-center gap-1.5 text-xs font-mono uppercase tracking-widest text-primary mb-2">
                  <Activity className="w-3.5 h-3.5" /> Step Review
                </p>
                <div className="space-y-3">
                  {lab.review.map((item) => (
                    <div key={item.step_id} className="rounded-xl border border-zinc-800 bg-zinc-950/60 p-3">
                      <div className="flex items-center justify-between gap-2 mb-1.5">
                        <p className="text-xs font-semibold text-zinc-200">{item.title}</p>
                        {item.correct ? (
                          <span className="flex items-center gap-1 text-[10px] font-mono uppercase tracking-wider text-emerald-400">
                            <CheckCircle2 className="w-3 h-3" /> Correct
                          </span>
                        ) : (
                          <span className="flex items-center gap-1 text-[10px] font-mono uppercase tracking-wider text-rose-400">
                            <XCircle className="w-3 h-3" /> Incorrect
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-zinc-400 mb-1.5">
                        <span className="text-zinc-500">Q:</span> {item.question}
                      </p>
                      <p className="text-xs text-zinc-300 mb-1">
                        <span className="text-zinc-500">Your answer:</span> {item.user_answer || '(no answer)'}
                      </p>
                      <p className="text-xs text-zinc-300">
                        <span className="text-zinc-500">Correct answer:</span> {item.correct_answer}
                      </p>
                      {item.explanation && (
                        <p className="text-xs text-zinc-400 mt-1.5 leading-relaxed">{item.explanation}</p>
                      )}
                      <p className="text-[10px] font-mono text-zinc-500 mt-1.5">
                        Hints used: {item.hints_used} · Attempts: {item.attempts}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <Button
              size="sm"
              variant="outline"
              disabled={disabled}
              onClick={onRestart}
              className="gap-1.5 text-muted-foreground"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Run again
            </Button>
          </div>
        ) : (
          <>
            <p className="text-sm sm:text-base text-zinc-100 leading-relaxed">
              {lab.current_question}
            </p>

            <div className="mt-4 flex gap-2">
              <input
                value={draft}
                disabled={disabled}
                onChange={(e) => setDraft(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && submit()}
                placeholder="Type your answer..."
                className="flex-1 rounded-xl border border-zinc-700 bg-zinc-900/70 px-3 py-2.5 text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/30 disabled:opacity-50"
              />
              <Button size="icon" variant="outline" onClick={submit} disabled={disabled || !draft.trim()} className="h-10 w-10 shrink-0">
                <Send className="w-4 h-4" />
              </Button>
            </div>

            {/* Revealed hints render inline in the card (no chat messages) */}
            {Array.isArray(lab.hints) && lab.hints.length > 0 && (
              <div className="mt-3 space-y-2">
                {lab.hints.map((hint: string, i: number) => (
                  <div key={i} className="rounded-lg border border-primary/20 bg-primary/[0.06] px-3 py-2 flex items-start gap-2">
                    <Lightbulb className="w-3.5 h-3.5 text-primary mt-0.5 shrink-0" />
                    <div>
                      <p className="text-[10px] font-mono uppercase tracking-widest text-primary">Hint {i + 1}</p>
                      <p className="text-xs text-zinc-300 leading-relaxed">{hint}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className="flex items-center gap-2 mt-3">
              <Button
                size="sm"
                variant="ghost"
                disabled={disabled || lab.hints_used >= lab.hints_available}
                onClick={onHint}
                className="gap-1.5 text-muted-foreground hover:text-primary"
              >
                <Lightbulb className="w-3.5 h-3.5" />
                {lab.hints_used >= lab.hints_available ? 'No hints left' : 'Hint'}
                {lab.hints_used > 0 && (
                  <span className="text-[10px] font-mono text-muted-foreground">
                    {lab.hints_used}/{lab.hints_available}
                  </span>
                )}
              </Button>
              <span className="text-[10px] font-mono text-muted-foreground ml-auto">
                Score: {lab.score}/{lab.total}
              </span>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
