from django.urls import path
from .views import (
    course_list,
    course_detail,
    enroll,
    enrollment_status,
    course_access_token,
    lesson_progress,
    lesson_content,
    mark_lesson_complete,
    submit_quiz,
    course_completion,
    my_quiz_scores,
    submit_lab_answer,
)

urlpatterns = [
    path("", course_list, name="course-list"),
    path("<slug:slug>/", course_detail, name="course-detail"),
    path("<slug:slug>/enroll/", enroll, name="course-enroll"),
    path("<slug:slug>/enrollment/", enrollment_status, name="course-enrollment-status"),
    path("<slug:slug>/access-token/", course_access_token, name="course-access-token"),
    path("<slug:slug>/progress/", lesson_progress, name="course-lesson-progress"),
    path("<slug:slug>/completion/", course_completion, name="course-completion"),
    path("<slug:slug>/quiz-scores/", my_quiz_scores, name="course-quiz-scores"),
    path("<slug:slug>/quiz/<str:quiz_id>/submit/", submit_quiz, name="course-quiz-submit"),
    # Lesson endpoints — order matters: specific paths before parameterised ones.
    path(
        "<slug:slug>/lessons/<str:lesson_id>/content/",
        lesson_content,
        name="lesson-content",
    ),
    path(
        "<slug:slug>/lessons/<str:lesson_id>/complete/",
        mark_lesson_complete,
        name="course-lesson-complete",
    ),
    path(
        "<slug:slug>/lessons/<str:lesson_id>/lab-questions/<str:question_id>/submit/",
        submit_lab_answer,
        name="lab-question-submit",
    ),
]
