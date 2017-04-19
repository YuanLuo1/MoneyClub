from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request, error_message=None):
	return render(request, 'MoneyClub/home.html',{})

def load(request):
	return render(request, 'MoneyClub/index.html', {})