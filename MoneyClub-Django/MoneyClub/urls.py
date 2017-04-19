from django.conf.urls import include, url
from django.views.generic import RedirectView
import django.contrib.auth.views
import MoneyClub.views
import MoneyClub.forms
import django_messages.views

urlpatterns = [
     url(r'^$', MoneyClub.views.home,name='home'),
     url(r'^login$', django.contrib.auth.views.login, {'template_name':'MoneyClub/login.html', 'authentication_form': MoneyClub.forms.CustomAuthForm}, name='login'),
     url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    # url(r'^register$', MoneyClub.views.register, name='register'),
]