from django.http import HttpResponse
import requests

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def pokedex(request):
    return render(request, 'pokedex.html')

def team(request):
    return render(request, 'team.html')