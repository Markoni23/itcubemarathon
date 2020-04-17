from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.views.generic import (
    DetailView, 
    CreateView,
    UpdateView,
)
from .models import *
from .forms import LessonForm, CourseForm

# Create your views here.

def index(request):
    return render(request, 'index.html', context = {
                                            'tile':'Главная',
                                            'courses': Course.objects.all(),
                                        })


def teachers(request):
    return render(request, 'teachers.html', context = {'teachers': Teacher.objects.all()})

def check_student(user):
    try:
        if user.student:
            return True
    except:
        pass
    return False

def check_teacher(user):
    try:
        if user.teacher:
            return True
    except:
        pass
    return False


@user_passes_test(check_student)
def register_to_course(request, course_pk):
    student = request.user.student
    course = Course.objects.get(pk=course_pk)
    student.courses.add(course)
    student.save()
    messages.success(request,f"Вы успешно записались на курс '{course.title}'!")
    return redirect('course', pk=course.pk)

@user_passes_test(check_teacher)
def course_statistic(request, course_pk):
    course = Course.objects.get(pk=course_pk)
    return render(request, 'marathon/course_statistic.html', context={'course': course})




class CourseView(DetailView):
    model = Course
    

class CourseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Course
    form_class = CourseForm

    def form_valid(self, form):
        form.instance.teacher = self.request.user.teacher
        return super().form_valid(form)

    def test_func(self):
        try:
            if self.request.user.teacher:
                return True
        except:
            return False


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    form_class = CourseForm

    def form_valid(self, form):
        form.instance.teacher = self.request.user.teacher
        return super().form_valid(form)

    def test_func(self):
        try:
            teacher = self.request.user.teacher
        except:
            return False
        return teacher == self.get_object().teacher


class LessonView(DetailView):
    model = Lesson

class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Lesson
    form_class = LessonForm

    def test_func(self):
        try:
            teacher = self.request.user.teacher
        except:
            return False
        course = Course.objects.get(pk=self.kwargs.get('pk'))
        return teacher == course.teacher


class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    form_class = LessonForm

    def form_valid(self, form):
        course = Course.objects.get(pk=self.kwargs.get('pk'))
        form.instance.course = course
        return super().form_valid(form)

    def test_func(self):
        try:
            teacher = self.request.user.teacher
        except:
            return False
        course = Course.objects.get(pk=self.kwargs.get('pk'))
        return teacher == course.teacher