from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, get_user

# Django transaction system so we can use @transaction.atomic
from django.db import transaction

# Imports from Model and Forms
from MoneyClub.models import *
from MoneyClub.forms import *

from datetime import datetime

from django.views.decorators.csrf import ensure_csrf_cookie
from django.core import serializers

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
# Used to send mail from within Django
from django.core.mail import send_mail
from dateutil import parser
from django.db import connection
from random import randint
import json
import googlemaps
import datetime
import math
import operator

# Create your views here.
def home(request, error_message=None):
    return render(request, 'MoneyClub/home.html',{})

def load(request):
    return render(request, 'MoneyClub/index_yl.html', {})

def timeline(request):
    return render(request, 'MoneyClub/timeline.html', {})

def stockvote(request):
    return render(request, 'MoneyClub/vote.html', {})

def education(request):
    return render(request, 'MoneyClub/education.html', {})

def charts(request):
    return render(request, 'MoneyClub/charts.html', {})

def history(request):
    return render(request, 'MoneyClub/history.html', {})

def president(request):
    return render(request, 'MoneyClub/president.html', {})

def secretary(request):
    return render(request, 'MoneyClub/secretary.html', {})

def treasurer(request):
    return render(request, 'MoneyClub/treasurer.html', {})

def profile(request):
    return render(request, 'MoneyClub/userprofile.html', {})

@transaction.atomic
def register(request):
    context = {}
    stock  =  Stock.objects.all()
    print(stock)
     # Just display the registration form if this is a GET request
    if request.method == 'GET':
        context['form'] = RegisterForm(auto_id=False)
        context['form_login'] = CustomAuthForm(auto_id=False)
        return render(request, 'MoneyClub/register.html', context)

    form = RegisterForm(request.POST, request.FILES)
    context['form_login'] = AuthenticationForm(auto_id=False)
    context['form'] = form
    if not form.is_valid():
        print(form.errors)
        return render(request, 'MoneyClub/register.html', context)

    # Creates the new user from the valid form data
    new_user = form.save(commit=False)
    new_user.is_active = False
    new_user.set_password(form.cleaned_data['password1'])
    new_user.save()
    context['user_id'] = new_user.id
    context['form'] = ProfileForm()
    context['form_login'] = AuthenticationForm(auto_id=False)

    token = default_token_generator.make_token(new_user)
    new_token = Token.objects.create(user=new_user, token=token)
    new_token.save()

    # Removed duplicates
    for row in Info.objects.all():
        if Info.objects.filter(username=new_user.username).count() > 1:
            row.delete()

    #user_profile = get_object_or_404(Info, owner=new_user)
    email_body = """
        Hi %s %s,\n\nWelcome to MoneyClub.
    Please click the link below to verify your email address and complete the registration of your account:

        http://%s%s
    """ % (new_user.first_name, new_user.last_name, request.get_host(),
           reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address for Money Club",
              message=email_body,
              from_email="yluo2+@andrew.cmu.edu",
              recipient_list=[new_user.email])
    return render(request, 'MoneyClub/email_conf.html', context)



@transaction.atomic
def confirm_register(request, username, token):
    context = {}
    try:
        user = get_object_or_404(User, username=username)
        # Removed duplicates
        for row in Token.objects.all():
            if Token.objects.filter(user=user).count() > 1:
                row.delete()

        old_token = Token.objects.get(user=user).token
        if old_token == token:
            user.is_active = True
            user.save()
            authenticate(username=user.username, password=user.password)
            context['success'] = "Congratulations! Now you can log in to your account!"
        else:
            context['error'] = "This is not the correct token generated for you!"
    except ObjectDoesNotExist:
        context['error'] = "OOOOps, The activation key does not exist."

    return render(request, 'MoneyClub/activation_confirmation.html', context)