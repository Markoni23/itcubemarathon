from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
#from tinymce.models import HTMLField
from testing.models import TestResult

# Create your models here.
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    info = models.TextField(max_length=255)
    avatar = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"Учитель: {self.user.last_name} {self.user.first_name} "

class Course(models.Model):
    title = models.CharField(max_length=255)
    short_info = models.TextField(max_length=500, default='Краткая информация о курсе')
    info = models.TextField()
    you_tube_url = models.CharField(max_length=50, default='', blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    secret_course = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'Направление: {self.title}'

    def get_absolute_url(self):
        return reverse('course', kwargs={'pk':self.pk})

    def get_comments(self):
        return self.comments.all()


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    #info = HTMLField()
    info = models.TextField()
    video = models.CharField(max_length=50, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk']

    def get_absolute_url(self):
        return reverse('lesson', kwargs={'pk':self.pk})

    def __str__(self):
        return f"Урок:{self.title}, курс: {self.course.title}"

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    info = models.TextField(max_length=255)
    courses = models.ManyToManyField(Course)
    secret_quest = models.BooleanField(default=False)
    age_category = models.ForeignKey("testing.AgeCategory", verbose_name="Возрастная категория", on_delete=models.CASCADE, null=True)

    def get_grades_for_course(self, course_pk):
        grades = {}
        for lesson in Course.objects.get(pk=course_pk).lesson_set.all():
            grades[lesson.id] = LessonMarks.objects.get_or_create(student=self, lesson=lesson)[0].value
        return grades

    def has_test(self, test):
        try:
            TestResult.objects.get(student=self, test=test)
            return True
        except TestResult.DoesNotExist:
            return False

    def get_test(self, test):
        if self.has_test(test):
            return TestResult.objects.get(student=self, test=test)
        else:
            return None

    def test_results(self, test):
        tr = self.get_test(test)
        if not tr:
            return None
        s = 0
        for resultanswer in tr.resultanswer_set.all():
            if resultanswer.selected_ans.right_ans:
                s += 1
            else:
                s -= 1
        return max(s, 0)

    def __str__(self):
        try:
            return f'Ученик: {self.user.last_name} {self.user.first_name}'
        except:
            return f'Ученик: {self.pk}'


class LessonMarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    value = models.IntegerField(default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])

class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    created_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f"Комм. к {self.course.title} от {self.author.username}"
    