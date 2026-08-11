from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Course, Enrollment, LessonProgress, QuizScore
from .quiz_answers import QUIZ_CORRECT_ANSWERS

User = get_user_model()

class CourseQuizTests(TestCase):
    fixtures = ["courses.json"]

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="User"
        )
        self.client.force_authenticate(user=self.user)

    def test_easy_level_courses_quizzes(self):
        # The three easy level courses slug list
        target_courses = [
            "blue-team-soc-fundamentals",
            "log-analysis-for-beginners",
            "siem-fundamentals"
        ]

        # Map slug to courseId keys used in QUIZ_CORRECT_ANSWERS
        slug_to_course_id = {
            "blue-team-soc-fundamentals": "soc-fundamentals",
            "log-analysis-for-beginners": "log-analysis",
            "siem-fundamentals": "siem-fundamentals"
        }

        for slug in target_courses:
            course = Course.objects.get(slug=slug)
            
            # Enroll and mark paid
            Enrollment.objects.create(
                user=self.user,
                course=course,
                is_paid=True
            )

            # Find all quizzes for this course in QUIZ_CORRECT_ANSWERS
            course_id = slug_to_course_id[slug]
            quizzes_to_test = []
            for (cid, qid) in QUIZ_CORRECT_ANSWERS.keys():
                if cid == course_id or cid == slug:
                    quizzes_to_test.append(qid)

            self.assertTrue(len(quizzes_to_test) > 0, f"No quizzes found for course {slug}")

            for quiz_id in quizzes_to_test:
                answer_key = QUIZ_CORRECT_ANSWERS.get((course_id, quiz_id)) or QUIZ_CORRECT_ANSWERS.get((slug, quiz_id))
                self.assertIsNotNone(answer_key, f"Answer key missing for {slug}/{quiz_id}")

                # Test 1: Submit correct answers
                submit_url = f"/api/courses/{slug}/quiz/{quiz_id}/submit/"
                response = self.client.post(submit_url, {"answers": answer_key}, format="json")
                
                self.assertEqual(
                    response.status_code, status.HTTP_200_OK,
                    f"Failed to submit correct answers for {slug}/{quiz_id}: {response.data}"
                )
                self.assertEqual(response.data["score"], 100)
                self.assertTrue(response.data["passed"])
                self.assertEqual(response.data["correct_count"], len(answer_key))

                # Verify DB updates
                score_obj = QuizScore.objects.filter(user=self.user, course_slug=slug, quiz_id=quiz_id).first()
                self.assertIsNotNone(score_obj)
                self.assertEqual(score_obj.score, 100)
                self.assertTrue(score_obj.passed)

                # Verify LessonProgress is updated for the quiz itself
                lp_quiz = LessonProgress.objects.filter(user=self.user, course=course, lesson_id=quiz_id).exists()
                self.assertTrue(lp_quiz, f"LessonProgress not created for quiz {quiz_id}")

                # Test 2: Submit wrong answers (all incorrect index)
                # Build an incorrect answer map
                wrong_answers = {qid: (ans_idx + 1) % 4 for qid, ans_idx in answer_key.items()}
                response_wrong = self.client.post(submit_url, {"answers": wrong_answers}, format="json")
                self.assertEqual(response_wrong.status_code, status.HTTP_200_OK)
                self.assertEqual(response_wrong.data["score"], 0)
                self.assertFalse(response_wrong.data["passed"])

                # Test 3: Multiple attempts — best score is kept (100% should remain)
                score_obj_check = QuizScore.objects.filter(user=self.user, course_slug=slug, quiz_id=quiz_id).first()
                self.assertEqual(score_obj_check.score, 100)

    def test_unauthorized_access(self):
        # Test that unauthorized user cannot submit quiz
        self.client.force_authenticate(user=None)
        course = Course.objects.get(slug="siem-fundamentals")
        submit_url = "/api/courses/siem-fundamentals/quiz/siem-q1/submit/"
        response = self.client.post(submit_url, {"answers": {}}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
