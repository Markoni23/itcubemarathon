from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
#from tinymce.models import HTMLField


# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    info = models.TextField(max_length=255)


class Course(models.Model):
    title = models.CharField(max_length=255)
    short_info = models.TextField(max_length=500, default='Краткая информация о курсе')
    info = models.TextField()
    you_tube_url = models.CharField(max_length=50, default='', blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('course', kwargs={'pk':self.pk})

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    #info = HTMLField()
    info = models.TextField(max_length=1000)
    video = models.CharField(max_length=50, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'pk':self.pk})

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    info = models.TextField(max_length=255)
    courses = models.ManyToManyField(Course)

    def get_grades_for_course(self, course_pk):
        grades = {}
        for lesson in Course.objects.get(pk=course_pk).lesson_set.all():
            grades[lesson.id] = LessonMarks.objects.get_or_create(student=self, lesson=lesson)[0].value
        return grades

class LessonMarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    value = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])