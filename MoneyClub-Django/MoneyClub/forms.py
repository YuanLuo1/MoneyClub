from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.safestring import mark_safe
from MoneyClub.models import *

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class': 'form-control form-signin','placeholder': 'Username', 'required': 'True'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class': 'form-control form-signin','placeholder':'Password', 'required':'True'}))