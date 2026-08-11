/**
 * labContext.ts — conversational practice labs in the AI Workspace.
 *
 * A "Start Lab" action is delivered to the chat backend as a structured
 * `context.lab` payload so routing is deterministic (no keyword guessing).
 * The backend routes it to the Lab Mentor engine which runs the interactive
 * practice flow. The catalog below mirrors the backend scenario registry.
 */

export interface LabContextPayload {
  action: 'start' | 'resume' | 'answer';
  lab_id?: string;
}

export interface PracticeLab {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  difficulty: string;
  category: string;
  estimatedMinutes: number;
}

export const PRACTICE_LABS: PracticeLab[] = [
  {
    id: 'phishing-email-analysis',
    title: 'Phishing Email Analysis',
    subtitle: 'Spot a credential-harvesting email and decide the response',
    description:
      'Analyze a suspicious PayPal email: the sender, the pressure tactics, the link, and the correct response.',
    difficulty: 'beginner',
    category: 'Email Security',
    estimatedMinutes: 6,
  },
  {
    id: 'siem-alert-triage',
    title: 'SIEM Alert Triage',
    subtitle: 'Triage a high-priority brute-force alert end to end',
    description:
      'Read a brute-force alert, recognize the pattern, scope the impact, and recommend containment.',
    difficulty: 'intermediate',
    category: 'SOC / Detection',
    estimatedMinutes: 8,
  },
];

export function buildLabStartContext(labId: string): LabContextPayload {
  return { action: 'start', lab_id: labId };
}

export function buildLabResumeContext(): LabContextPayload {
  return { action: 'resume' };
}

export function getPracticeLab(id: string): PracticeLab | undefined {
  return PRACTICE_LABS.find((l) => l.id === id);
}
