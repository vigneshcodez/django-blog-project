from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms


class CustomUserFrom(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ['username',  'email', 'password1', 'password2']
