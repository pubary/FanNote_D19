from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import FunUser


class FunUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Логин')
    email = forms.EmailField(label='E-mail')

    class Meta:
        model = FunUser
        fields = ['username',
                  'email',
                  'password1',
                  'password2',]


class FunUserChangeForm(UserChangeForm):
    pass
