from django.contrib import admin
from django.urls import path

from .views import index, teachers, register_to_course, course_statistic
from .views import (
    CourseView,
    CourseCreateView,
    CourseUpdateView,
    LessonView,
    LessonCreateView,
)

urlpatterns = [
    path('', index, name='home'),
    path('teachers', teachers, name='teachers'),
    path('course/<int:pk>', CourseView.as_view(), name='course'),
    path('course/<int:course_pk>/register', register_to_course, name='register-to-course'),
    path('course/<int:course_pk>/statistic', course_statistic, name='course-statistic'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('course/new/', CourseCreateView.as_view(), name='course-new'),
    path('lesson/<int:pk>', LessonView.as_view(), name='lesson'),
    path('course/<int:pk>/new_lesson', LessonCreateView.as_view(), name='lesson-new')
]