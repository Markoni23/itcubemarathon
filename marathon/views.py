from django.shortcuts import render
from django.views.generic import DetailView

from .models import *

# Create your views here.

def index(request):
    return render(request, 'index.html', context = {
                                            'tile':'Главная',
                                            'courses': Course.objects.all(),
                                        })

class CourseView(DetailView):
    model = Course
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Course.objects.all()
        return context