from django.http import HttpResponse
import requests

from django.shortcuts import render

def accueil(request):
    pokemon_list = get_pokemon_list()
    return render(request, 'pokemon_list.html', {'pokemon_list': pokemon_list})

def get_pokemon_list():
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        return []
