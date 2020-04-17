from django_summernote.widgets import SummernoteInplaceWidget
from django import forms
from .models import Lesson, Course

# If you don't like <iframe>, then use inplace widget
# Or if you're using django-crispy-forms, please use this.
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'info', 'video']
        widgets = {
            'info': SummernoteInplaceWidget(),
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'short_info', 'info', 'you_tube_url']
        widgets = {
            'info': SummernoteInplaceWidget(),
        }