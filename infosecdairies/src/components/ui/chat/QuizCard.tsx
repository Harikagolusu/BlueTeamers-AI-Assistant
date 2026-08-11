import React, { useState } from 'react';
import {
  Brain,
  CheckCircle2,
  XCircle,
  MinusCircle,
  Award,
  Sparkles,
  ArrowRight,
  RefreshCw,
  Send,
  Lightbulb,
} from 'lucide-react';
import { Button } from '@/components/ui/button';

const TYPE_LABELS: Record<string, string> = {
  mcq: 'Multiple Choice',
  true_false: 'True / False',
  fill_in_blank: 'Fill in the Blank',
  short_answer: 'Short Answer',
  scenario: 'Scenario',
  interview: 'Interview',
  code: 'Code',
};

const OPTION_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F'];

export const QuizCard: React.FC<{
  quiz: any;
  disabled?: boolean;
  onAnswer: (answer: string) => void;
}> = ({ quiz, disabled, onAnswer }) => {
  const [draft, setDraft] = useState('');
  if (!quiz) return null;

  const hasOptions = Array.isArray(quiz.options) && quiz.options.length > 0;
  const freeText = !hasOptions;

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
            <Brain className="w-4 h-4 text-primary" />
          </span>
          <div>
            <p className="text-xs font-mono uppercase tracking-widest text-primary">Quiz Mode</p>
            <p className="text-[10px] text-muted-foreground font-mono">
              Question {quiz.index} of {quiz.total}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {quiz.difficulty && (
            <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground px-2 py-0.5 rounded-md border border-border/60 bg-zinc-950/60">
              {quiz.difficulty}
            </span>
          )}
          <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground px-2 py-0.5 rounded-md border border-border/60 bg-zinc-950/60">
            {TYPE_LABELS[quiz.type] || 'Question'}
          </span>
        </div>
      </div>

      {/* Question */}
      <div className="px-4 py-4">
        <p className="text-sm sm:text-base text-zinc-100 leading-relaxed">{quiz.text}</p>

        {hasOptions ? (
          <div className="grid grid-cols-1 gap-2 mt-4">
            {quiz.options.map((opt: string, i: number) => (
              <button
                key={i}
                disabled={disabled}
                onClick={() => onAnswer(OPTION_LETTERS[i] || opt)}
                className="group flex items-center gap-3 rounded-xl border border-zinc-700/80 bg-zinc-900/60 hover:border-primary/50 hover:bg-primary/10 disabled:opacity-50 disabled:hover:border-zinc-700/80 disabled:hover:bg-zinc-900/60 transition-all text-left px-3 py-2.5"
              >
                <span className="w-6 h-6 shrink-0 rounded-md border border-zinc-600 bg-zinc-950/70 text-[11px] font-mono text-primary flex items-center justify-center group-hover:border-primary/50">
                  {OPTION_LETTERS[i] || i + 1}
                </span>
                <span className="text-sm text-zinc-200 group-hover:text-zinc-100">{opt}</span>
              </button>
            ))}
          </div>
        ) : (
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
        )}
      </div>
    </div>
  );
};

export const QuizOfferCard: React.FC<{
  topic?: string;
  disabled?: boolean;
  onStart: () => void;
  onSkip: () => void;
}> = ({ topic, disabled, onStart, onSkip }) => {
  return (
    <div className="mt-2 w-full max-w-[560px] not-prose rounded-2xl border border-primary/25 bg-gradient-to-b from-zinc-900/95 to-zinc-950/95 shadow-[0_0_25px_rgba(0,186,216,0.08)] overflow-hidden">
      <div className="px-4 py-4">
        <div className="flex items-center gap-3 mb-3">
          <span className="w-9 h-9 rounded-xl bg-primary/15 border border-primary/30 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-primary" />
          </span>
          <div>
            <p className="text-sm font-semibold text-zinc-100">Ready to practice?</p>
            {topic && (
              <p className="text-xs font-mono text-muted-foreground">Topic: {topic}</p>
            )}
          </div>
        </div>
        <p className="text-sm text-zinc-300 leading-relaxed">
          Would you like to test your understanding with a short quiz? I can help you
          practice this concept with a few questions.
        </p>
        <div className="flex gap-2 mt-4">
          <Button
            size="sm"
            disabled={disabled}
            onClick={onStart}
            className="gap-1.5 bg-primary text-primary-foreground hover:bg-primary/90"
          >
            Start quiz <ArrowRight className="w-3.5 h-3.5" />
          </Button>
          <Button
            size="sm"
            variant="ghost"
            disabled={disabled}
            onClick={onSkip}
            className="text-muted-foreground"
          >
            Not now
          </Button>
        </div>
      </div>
    </div>
  );
};

export const QuizResultCard: React.FC<{
  result: any;
  disabled?: boolean;
  onRetake: () => void;
}> = ({ result, disabled, onRetake }) => {
  if (!result) return null;
  const pct = result.total > 0 ? Math.round((result.score / result.total) * 100) : 0;
  const tone = result.passed
    ? 'border-emerald-500/30 text-emerald-400'
    : 'border-amber-500/30 text-amber-400';

  return (
    <div className="mt-2 w-full max-w-[560px] not-prose rounded-2xl border border-primary/25 bg-gradient-to-b from-zinc-900/95 to-zinc-950/95 shadow-[0_0_25px_rgba(0,186,216,0.08)] overflow-hidden">
      <div className="px-4 py-4 border-b border-primary/15 bg-primary/[0.06]">
        <div className="flex items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-primary" />
            <p className="text-sm font-semibold text-zinc-100">Assessment Complete</p>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-zinc-50 leading-none">
              {result.score}
              <span className="text-base text-muted-foreground font-mono"> / {result.total}</span>
            </p>
            <p className="text-[10px] font-mono text-muted-foreground mt-1">{pct}%</p>
          </div>
        </div>
      </div>

      <div className="px-4 py-4 space-y-4">
        <div className={`inline-flex items-center gap-1.5 rounded-lg border px-2.5 py-1 text-xs font-mono uppercase tracking-wider ${tone}`}>
          {result.passed ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
          {result.passed ? 'Passed' : 'Keep practicing'}
        </div>

        <div>
          <p className="flex items-center gap-1.5 text-xs font-mono uppercase tracking-widest text-emerald-400 mb-2">
            <CheckCircle2 className="w-3.5 h-3.5" /> Strengths
          </p>
          <ul className="space-y-1">
            {(result.strengths || []).map((s: string, i: number) => (
              <li key={i} className="text-sm text-zinc-300 flex gap-2">
                <span className="text-emerald-500">+</span> {s}
              </li>
            ))}
          </ul>
        </div>

        <div>
          <p className="flex items-center gap-1.5 text-xs font-mono uppercase tracking-widest text-amber-400 mb-2">
            <MinusCircle className="w-3.5 h-3.5" /> Needs Improvement
          </p>
          <ul className="space-y-1">
            {(result.weak_areas || []).map((w: string, i: number) => (
              <li key={i} className="text-sm text-zinc-300 flex gap-2">
                <span className="text-amber-500">-</span> {w}
              </li>
            ))}
          </ul>
        </div>

        {(result.recommendations || []).length > 0 && (
          <div>
            <p className="flex items-center gap-1.5 text-xs font-mono uppercase tracking-widest text-primary mb-2">
              <Lightbulb className="w-3.5 h-3.5" /> Recommendations
            </p>
            <ul className="space-y-1">
              {(result.recommendations || []).map((r: string, i: number) => (
                <li key={i} className="text-sm text-zinc-400 flex gap-2">
                  <span className="text-primary">-</span> {r}
                </li>
              ))}
            </ul>
          </div>
        )}

        {result.next_topic && (
          <div className="rounded-xl border border-primary/20 bg-primary/[0.05] px-3 py-2.5 flex items-start gap-2">
            <ArrowRight className="w-4 h-4 text-primary mt-0.5 shrink-0" />
            <div>
              <p className="text-[10px] font-mono uppercase tracking-widest text-muted-foreground">Recommended Next Topic</p>
              <p className="text-sm text-zinc-200">{result.next_topic}</p>
            </div>
          </div>
        )}

        <Button
          size="sm"
          variant="outline"
          disabled={disabled}
          onClick={onRetake}
          className="gap-1.5 w-full text-muted-foreground"
        >
          <RefreshCw className="w-3.5 h-3.5" /> Another quiz
        </Button>
      </div>
    </div>
  );
};
