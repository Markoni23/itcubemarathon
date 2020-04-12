from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('course/<int:pk>', CourseView.as_view(), name='course'),
]