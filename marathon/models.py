from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    info = models.TextField(max_length=255)

class Course(models.Model):
    title = models.CharField(max_length=255)
    short_info = models.TextField(max_length=500, default='Краткая информация о курсе')
    info = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    info = models.TextField()
    video = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)