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

class RegisterForm(forms.ModelForm):
    password1=forms.CharField(max_length=200,label='', \
        widget=forms.PasswordInput(attrs={'class':'form-control', \
            'placeholder':'Confirm Password', 'required':True, 'autofocus':True }))
    class Meta:
        model=User
        fields={'email','username','password','password1'}
        widgets={
            'email': forms.EmailInput(attrs={'class':'form-control', \
            'placeholder':'Email', 'required':True, 'autofocus':True }), \
            'username':forms.TextInput(attrs={'class':'form-control', \
            'placeholder':'Username', 'required':True, 'autofocus':True }), \
            'password':forms.PasswordInput(attrs={'class':'form-control', \
            'placeholder':'Password','required':True, 'autofocus':True })
        }
        labels={'email':'','username':'','password':'','password1':''}
        help_texts={'username':''}

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.order_fields([
            'email',
            'username',
            'password',
            'password1'])


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Info
        exclude = ('owner', 'username', 'email', 'profile_img',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',\
                                                'placeholder': 'First name', 'required': True, 'autofocus': True}), \
            'last_name': forms.TextInput(attrs={'class': 'form-control',\
                                                'placeholder': 'Last name', 'required': True}), \
            'age': forms.NumberInput(attrs={'class': 'form-control', \
                                            'placeholder': 'Age', 'required': True}), \
            'city': forms.TextInput(attrs={'class': 'form-control', \
                                           'placeholder': 'City', 'required': False}), \
            'short_bio': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', \
                                               'placeholder': 'Short bio', 'required': False}), \
            }

        labels = {'first_name': '', 'last_name': '', 'age': '', 'city': '', 'short_bio': '', }

        def clean(self):
            cleaned_data = super(ProfileForm, self).clean()
            return cleaned_data