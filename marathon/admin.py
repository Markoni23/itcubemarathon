from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *
# Register your models here.

class LessonAdmin(SummernoteModelAdmin):
    summernote_fields = ('info',)

admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Student)