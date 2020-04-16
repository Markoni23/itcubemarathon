from django import forms
from django.conf import settings 
from marathon.models import Teacher
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


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