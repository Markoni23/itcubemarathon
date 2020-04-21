from django import forms
from django.conf import settings 
from marathon.models import Teacher, Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import password_validation
from django.forms.widgets import PasswordInput, TextInput
from django.forms import ValidationError


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя/email')
    password = forms.CharField(label='Пароль',widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    agree = forms.BooleanField(label='Согласие на обработку <a href="https://google.com">персональных данных</a>')
    first_name = forms.CharField(max_length=25, label = 'Имя')
    last_name = forms.CharField(max_length=100, label = 'Фамилия')
    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput,
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        strip=False,
        widget=forms.PasswordInput,
    )
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name', 'password1', 'password2', 'agree']
        labels = {
                "username": "Имя пользователя",
            }


class CreateTeacher(forms.Form):
    secret_key = forms.CharField(label='Очень секретный пароль', max_length=100)
    
    def clean_secret_key(self):
        secret_key = self.cleaned_data['secret_key']
        if secret_key != settings.SECRET_KEY_FOR_TEACHER:
            raise ValidationError('Очень секретный пароль не подходит')
        return secret_key

    def save(self, request):
        _, new = Teacher.objects.get_or_create(user = request.user, info='')
        return new

class CreateSecret(forms.Form):
    secret_key = forms.CharField(label='Очень секретный пароль', max_length=100)
    
    def clean_secret_key(self):
        secret_key = self.cleaned_data['secret_key']
        if secret_key != settings.SECRET_KEY_FOR_STUDENT:
            raise ValidationError('Очень секретный пароль не подходит')
        return secret_key

    def save(self, request):
        s = Student.objects.get(user=request.user)
        s.secret_quest = True
        s.save()
        return s