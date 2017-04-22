from django.shortcuts import render
from django.http import HttpResponse
from MoneyClub.models import *
from MoneyClub.forms import *
from django.http import HttpResponse, Http404
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def home(request, error_message=None):
    return render(request, 'MoneyClub/home.html',{})

def load(request):
    return render(request, 'MoneyClub/index.html', {})

@transaction.atomic
def register(request):
    context = {}

     # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegisterForm(auto_id=False)
        context['form_login'] = CustomAuthForm(auto_id=False)
        return render(request, 'skilltree/signup_step1.html', context)

    form = RegisterForm(request.POST, request.FILES)
    context['form_login'] = AuthenticationForm(auto_id=False)
    context['form'] = form
    if not form.is_valid():
        print(form.errors)
        return render(request, 'skilltree/signup_step1.html', context)

    # Creates the new user from the valid form data
    new_user = form.save(commit=False)
    new_user.is_active = False
    new_user.set_password(form.cleaned_data['password1'])
    new_user.save()
    context['user_id'] = new_user.id
    context['form'] = ProfileForm()
    context['form_login'] = AuthenticationForm(auto_id=False)
    return render(request, 'skilltree/signup_step2.html', context)