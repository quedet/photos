from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username (e.g. angelazard)', 'class': 'form--input'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': 'form--input'}),
        }


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username (e.g. angelazard)', 'class': 'form--input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address (e.g. angelazard@xyz.com)', 'class': 'form--input'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Create new password', 'class': 'form--input'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Repeat that password', 'class': 'form--input'}),
        }
