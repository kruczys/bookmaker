from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, label="login")
    password = forms.CharField(widget=forms.PasswordInput, label="haslo")
