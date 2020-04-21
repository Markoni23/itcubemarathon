from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core import serializers
from django.views.generic import (
    DetailView, 
    CreateView,
    UpdateView,
)
from .models import (
    Teacher,
    Student,
    Course,
    Lesson,
    CourseComment,
    LessonMarks
)
from .forms import LessonForm, CourseForm
from testing.models import *

# Create your views here.

def index(request):
    return render(request, 'index.html', context = {
                                            'tile':'Главная',
                                            'courses': Course.objects.filter(secret_course=False, active=True),
                                            'secret_courses': Course.objects.filter(secret_course=True, active=True),
                                            'teachers': Teacher.objects.all(),
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


def add_comment_to_course(request):
    print(request)
    print(request.POST)
    data = request.POST
    print(data.get('body'))
    comment = CourseComment.objects.create(
        author = request.user,
        body = data.get('body'),
        course = Course.objects.get(pk=data.get('course'))
    )
    return JsonResponse(serializers.serialize('json', [comment]), safe=False)


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

def get_test_results(request, pk):
    test = Test.objects.get(pk=pk)
    tr, _ = TestResult.objects.update_or_create(test=test, student=request.user.student)
    for question in test.question_set.all():
        if question.multiple:
            ans_list = request.POST.getlist(str(question.pk))
            if ans_list[0] != [0]:
                for ans in ans_list:
                    ResultAnswer.objects.update_or_create(testresult=tr, 
                                                selected_ans=Answer.objects.get(pk=int(ans)))
        else:
            ans = int(request.POST.get(str(question.pk), [0])[0])
            if ans != 0:
                ResultAnswer.objects.update_or_create(testresult=tr, 
                                                selected_ans=Answer.objects.get(pk=ans))
    return redirect('lesson', pk=test.lesson.pk)



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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            student = self.request.user.student
            if student.age_category:
                lesson = self.get_object()
                test = lesson.test_set.get(lesson=lesson,
                                                      category=student.age_category)
                
            else:
                test = lesson.test_set.first()
            context['test'] = test
            context['already_done_test'] = student.has_test(test)
            context['test_result'] = student.test_results(test)
        except:
            pass
        print(context)
        return context
    



class LessonCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
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


class LessonUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Lesson
    form_class = LessonForm

    def form_valid(self, form):
        course = self.get_object().course
        form.instance.course = course
        return super().form_valid(form)

    def test_func(self):
        try:
            teacher = self.request.user.teacher
        except:
            return False
        course = self.get_object().course
        return teacher == course.teacher