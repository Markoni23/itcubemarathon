from django.contrib import admin
from django.urls import path

from django.views.generic import RedirectView

from .views import (index, teachers, register_to_course, course_statistic, add_comment_to_course,
                    get_test_results)
from .views import (
    CourseView,
    CourseCreateView,
    CourseUpdateView,
    LessonView,
    LessonCreateView,
    LessonUpdateView,
)

urlpatterns = [
    path('', RedirectView.as_view(url='home'), name='home'),
    path('home', index),
    path('teachers', teachers, name='teachers'),
    path('course/<int:pk>', CourseView.as_view(), name='course'),
    path('addcoursecomment/', add_comment_to_course, name='add-comment-course'),
    path('course/<int:course_pk>/register', register_to_course, name='register-to-course'),
    path('course/<int:course_pk>/statistic', course_statistic, name='course-statistic'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('course/new/', CourseCreateView.as_view(), name='course-new'),
    path('lesson/<int:pk>', LessonView.as_view(), name='lesson'),
    path('lesson/<int:pk>/update', LessonUpdateView.as_view(), name='lesson-update'),
    path('course/<int:pk>/new_lesson', LessonCreateView.as_view(), name='lesson-new'),
    path('testresults/<int:pk>', get_test_results, name="test-results"),
]
