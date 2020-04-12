from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('course/<int:pk>', CourseView.as_view(), name='course'),
    path('lesson/<int:pk>', LessonView.as_view(), name='lesson'),
]