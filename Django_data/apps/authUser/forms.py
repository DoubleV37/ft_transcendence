from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class SignInForm(forms.Form):
    username = forms.CharField(
            max_length=30,
            widget=forms.TextInput(attrs={'placeholder':
                                          'Enter your username'}),
            )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder':
                                              'Enter your password'}),
            help_text=password_validation.password_validators_help_text_html(),
            )
