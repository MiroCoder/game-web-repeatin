from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, welcome to the biggest web of games")
# Create your views here.
