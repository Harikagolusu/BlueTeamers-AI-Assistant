import threading
from datetime import datetime
from typing import Dict, List, Optional

from app.agents.assessment.models import AssessmentProfile, DifficultyLevel, QuizResult


class InMemoryAssessmentProfileStore:
    """Per-user learning memory for the Assessment Agent.

    Tracks quiz history, topics completed, weak/strong topics, difficulty reached,
    average score, last assessment and overall progress. In-memory for now with a
    simple keyed interface so a persistent store can be substituted later.
    """

    def __init__(self):
        self._profiles: Dict[str, AssessmentProfile] = {}
        self._lock = threading.RLock()

    def get_or_create(self, user_key: str) -> AssessmentProfile:
        with self._lock:
            profile = self._profiles.get(user_key)
            if profile is None:
                profile = AssessmentProfile(user_key=user_key)
                self._profiles[user_key] = profile
            return profile.model_copy(deep=True)

    def save(self, profile: AssessmentProfile) -> None:
        with self._lock:
            self._profiles[profile.user_key] = profile.model_copy(deep=True)

    def record_result(
        self,
        user_key: str,
        result: QuizResult,
        topic: str,
        course_slug: Optional[str] = None,
    ) -> AssessmentProfile:
        profile = self.get_or_create(user_key)

        normalized_topic = (topic or "").strip().lower()
        topics = set(t.lower() for t in profile.topics_completed)
        topics.add(normalized_topic)
        profile.topics_completed = sorted(topics)

        for strong in result.strengths:
            s = strong.strip().lower()
            if s:
                profile.strong_topics = _merge(profile.strong_topics, s)
                profile.weak_topics = _remove(profile.weak_topics, s)
        for weak in result.weak_areas:
            w = weak.strip().lower()
            if w:
                profile.weak_topics = _merge(profile.weak_topics, w)
                profile.strong_topics = _remove(profile.strong_topics, w)
                if course_slug:
                    profile.revision_topics = _merge(
                        profile.revision_topics, f"{course_slug}:{w}"
                    )

        level_rank = list(DifficultyLevel)
        try:
            reached = DifficultyLevel(result.difficulty_reached)
            current = DifficultyLevel(profile.difficulty_reached)
            if level_rank.index(reached) > level_rank.index(current):
                profile.difficulty_reached = reached
        except ValueError:
            pass

        profile.assessment_count += 1
        total = profile.average_score * (profile.assessment_count - 1) + result.score
        profile.average_score = round(total / profile.assessment_count, 2)
        profile.last_assessment_at = datetime.utcnow()

        profile.quiz_history.append({
            "topic": topic,
            "course_slug": course_slug,
            "score": result.score,
            "total": result.total,
            "passed": result.passed,
            "difficulty": result.difficulty_reached.value,
            "at": profile.last_assessment_at.isoformat(),
        })

        profile.progress = {
            "assessments_completed": profile.assessment_count,
            "average_score": profile.average_score,
            "difficulty_reached": profile.difficulty_reached.value,
            "topics_completed": len(profile.topics_completed),
        }

        if course_slug:
            self._record_course_progress(profile, course_slug, result)

        self.save(profile)
        return profile.model_copy(deep=True)

    def _record_course_progress(
        self,
        profile: AssessmentProfile,
        course_slug: str,
        result: QuizResult,
    ) -> None:
        """Track per-course assessment history, weak/strong topics & completion."""
        slug = (course_slug or "").strip().lower()
        if not slug:
            return
        entry = dict(profile.course_progress.get(slug) or {})
        assessments = int(entry.get("assessments_completed", 0)) + 1
        avg_total = float(entry.get("average_score", 0.0)) * (assessments - 1) + result.score
        avg = round(avg_total / assessments, 2)

        strong = set(entry.get("strong_topics", [])) | {s.lower() for s in result.strengths}
        weak = set(entry.get("weak_topics", [])) | {w.lower() for w in result.weak_areas}

        entry.update({
            "assessments_completed": assessments,
            "average_score": avg,
            "last_assessment_at": profile.last_assessment_at.isoformat(),
            "strong_topics": sorted(strong),
            "weak_topics": sorted(weak),
            # A course is considered "complete" once the learner passes consistently.
            "complete": bool(result.passed and assessments >= 2),
        })
        profile.course_progress[slug] = entry

        # Overall completion = fraction of assessed courses that are complete.
        total_courses = len(profile.course_progress)
        completed = sum(1 for c in profile.course_progress.values() if c.get("complete"))
        profile.completion_percentage = round((completed / total_courses) * 100, 1) if total_courses else 0.0

    def get_recent_course_assessment(
        self,
        user_key: str,
        course_slug: str,
        limit: int = 5,
    ) -> List[Dict]:
        """Most recent quiz history entries for a specific course."""
        profile = self.get_or_create(user_key)
        slug = (course_slug or "").strip().lower()
        return [
            h for h in profile.quiz_history
            if h.get("course_slug") and str(h.get("course_slug")).strip().lower() == slug
        ][-limit:]

    def get_previous_topics(self, user_key: str, limit: int = 10) -> List[str]:
        profile = self.get_or_create(user_key)
        return profile.topics_completed[-limit:]


def _merge(items: List[str], value: str) -> List[str]:
    result = list(items)
    if value not in result:
        result.append(value)
    return result


def _remove(items: List[str], value: str) -> List[str]:
    return [i for i in items if i != value]
