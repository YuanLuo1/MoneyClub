from django.conf.urls import include, url
from django.contrib import admin
import MoneyClub.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^moneyclub/', include('MoneyClub.urls')),
    url(r'^$', MoneyClub.views.home),
    url(r'^messages/', include('django_messages.urls')),
]

