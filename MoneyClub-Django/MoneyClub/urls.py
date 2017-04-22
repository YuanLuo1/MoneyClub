from django.conf.urls import include, url
from django.views.generic import RedirectView
import django.contrib.auth.views
import MoneyClub.views
import MoneyClub.forms
import django_messages.views

urlpatterns = [
    url(r'^$', MoneyClub.views.home,name='home'),
    url(r'^login$', django.contrib.auth.views.login, {'template_name':'MoneyClub/login_yl.html', 'authentication_form': MoneyClub.forms.CustomAuthForm}, name='login'),
    url(r'^logout$', django.contrib.auth.views.logout_then_login, name='logout'),
    url(r'^register$', MoneyClub.views.register, name='register'),
    url(r'^confirm-register/(?P<username>\w+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', MoneyClub.views.confirm_register, name='confirm'),
    url(r'^reset/password_reset/$', django.contrib.auth.views.password_reset, {'template_name': 'MoneyClub/password_reset_form.html', 'password_reset_form': MoneyClub.forms.CustomPassResetEmail}, name="password_reset"),
    url(r'^dashboard$',MoneyClub.views.load, name = 'dashboard'),
    url(r'^dashboard/timeline$',MoneyClub.views.timeline, name = 'timeline'),
    url(r'^dashboard/stockvotes$',MoneyClub.views.stockvote, name = 'stockvote'),
    url(r'^dashboard/education$',MoneyClub.views.education, name = 'education'),
    url(r'^dashboard/charts$',MoneyClub.views.charts, name = 'charts'),
    url(r'^dashboard/history$',MoneyClub.views.history, name = 'history'),
    url(r'^dashboard/president$',MoneyClub.views.president, name = 'president'),
    url(r'^dashboard/secretary$',MoneyClub.views.secretary, name = 'secretary'),
    url(r'^dashboard/treasurer$',MoneyClub.views.treasurer, name = 'treasurer'),
    url(r'^messages/$', RedirectView.as_view(permanent=True, url='inbox/'), name='messages_redirect'),
    url(r'^messages/inbox/$', django_messages.views.inbox, {'template_name': 'django_messages/inbox.html'}, name='messages_inbox'),
    url(r'^messages/outbox/$', django_messages.views.outbox, {'template_name': 'django_messages/outbox.html'}, name='messages_outbox'),
    url(r'^messages/compose/$', django_messages.views.compose, {'template_name': 'django_messages/compose.html'}, name='messages_compose'),     url(r'^messages/compose/(?P<recipient>[\w.@+-]+)/$', django_messages.views.compose, {'template_name': 'django_messages/compose.html'}, name='messages_compose_to'),
    url(r'^messages/reply/(?P<message_id>[\d]+)/$', django_messages.views.reply, {'template_name': 'django_messages/compose.html'}, name='messages_reply'),
    url(r'^messages/view/(?P<message_id>[\d]+)/$', django_messages.views.view, {'template_name': 'django_messages/view.html'}, name='messages_detail'),
    url(r'^messages/delete/(?P<message_id>[\d]+)/$', django_messages.views.delete, name='messages_delete'),
    url(r'^messages/undelete/(?P<message_id>[\d]+)/$', django_messages.views.undelete, name='messages_undelete'),
    url(r'^messages/trash/$', django_messages.views.trash, {'template_name': 'django_messages/trash.html'}, name='messages_trash'),
]