from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, CreateTeacher
from django.contrib.auth.decorators import login_required

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Профиль успешно создан '{username}', теперь Вы можете войти!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', context={'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def became_teacher(request):
    if request.method == 'POST':
        form = CreateTeacher(request.POST)
        if form.is_valid():
            new = form.save(request)
            if new:
                messages.success(request,f"За Вами успешно закреплены права педагога")
            else:
                messages.success(request,f"Вы уже педагог!!!")
            return redirect('profile')
    else:
        form = CreateTeacher()
    return render(request, 'users/became_teacher.html', context={'form': form})