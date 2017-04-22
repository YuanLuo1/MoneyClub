from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse, resolve
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

    context = {}
    new_user = get_object_or_404(User, id=id)
    token = default_token_generator.make_token(new_user)
    new_token = Token.objects.create(user=new_user, token=token)
    new_token.save()

    # Removed duplicates
    for row in Info.objects.all():
        if Info.objects.filter(username=new_user.username).count() > 1:
            row.delete()

    user_profile = get_object_or_404(Info, owner=new_user)
    email_body = """
        Hi %s %s,\n\nWelcome to MoneyClub.
    Please click the link below to verify your email address and complete the registration of your account:

        http://%s%s
    """ % (user_profile.first_name, user_profile.last_name, request.get_host(),
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