from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.safestring import mark_safe
from MoneyClub.models import *

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'fontawesome-user','placeholder': 'Username', 'required': 'True'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'fontawesome-lock','placeholder':'Password', 'required':'True'}))

class CustomPassResetEmail(PasswordResetForm):
    email = forms.EmailField(max_length = 100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required':'True', 'style': 'margin-bottom: 10px'}))