export interface Lesson {
  id: string;
  title: string;
  description?: string;
  duration?: string;
  status: "completed" | "unlocked" | "locked";
}

export interface Module {
  id: string;
  title: string;
  badge?: string;
  badgeColor?: string;
  lessons: Lesson[];
  quizId?: string;
}

export interface Quiz {
  id: string;
  title: string;
  description: string;
  questionCount: number;
  passingScore: number;
  duration: string;
  status: "completed" | "unlocked" | "locked";
}

export interface Resource {
  id: string;
  title: string;
  description: string;
  type: "pdf" | "cheatsheet" | "template" | "tool" | "link";
  url?: string;
}

export interface Course {
  id: string;
  title: string;
  shortTitle: string;
  description: string;
  difficulty: "easy" | "medium" | "hard";
  duration: string;
  bgImage: string;
  modules: Module[];
  quizzes?: Quiz[];
  resources?: Resource[];
}
