from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, CreateTeacher, CreateSecret
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from marathon.models import Student

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token
from django.core.mail import EmailMessage
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False   
            user.save()
            Student.objects.create(user=user)
            current_site = get_current_site(request)
            mail_subject = 'Активируйте свою учетную запись в IT-Марафоне.'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            print(message)
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Профиль '{username}' почти создан , теперь осталось подтвердить регистрацию")
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/registration.html', context={'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request,f"Почта успешно подтверждена")
        return redirect('home')
    else:
        messages.success(request,f"Почта успешно подтверждена")
        return redirect('home')


@login_required
def profile(request):
    return render(request, 'users/profile.html')


@login_required
def became_teacher(request):
    if request.method == 'POST':
        form = CreateTeacher(request.POST)
        if form.is_valid():
            Student.objects.get(pk= request.user.student.pk).delete()
            new = form.save(request)
            if new:
                messages.success(request,f"За Вами успешно закреплены права педагога")
            else:
                messages.success(request,f"Вы уже педагог!!!")
            return redirect('profile')
    else:
        form = CreateTeacher()
    return render(request, 'users/became_teacher.html', context={'form': form})

@login_required
def became_secret(request):
    if request.method == 'POST':
        form = CreateSecret(request.POST)
        if form.is_valid():
            new = form.save(request)
            if new:
                messages.success(request,f"Теперь вы можете участвовать в секретном квесте!")
            else:
                messages.success(request,f"Что-то пошло не так, если видите это, напишите нам")
            return redirect('profile')
    else:
        form = CreateSecret()
    return render(request, 'users/became_teacher.html', context={'form': form})