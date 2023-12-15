import asyncio
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import requests
from django.core.cache import cache
from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.core.cache import cache
from MonApplication.request.get_pokemon import fetch_pokemon_data

def home(request):
    return render(request, 'home.html')

async def pokedex(request):
    pokemon_data = await get_cached_pokemon_data()
     # Récupère l'ID du Pokémon à partir de la requête GET, par défaut le premier Pokémon
    pokemon_id = request.GET.get('pokemon_id', 1)

    # Trouve le Pokémon correspondant ou renvoie le premier par défaut
    current_pokemon = next((pokemon for pokemon in pokemon_data if pokemon['id'] == int(pokemon_id)), pokemon_data[0])

    query = request.GET.get('search', '')
    if query:
        pokemon_data = [pokemon for pokemon in pokemon_data if query.lower() in pokemon['name'].lower()]
    return render(request, 'pokedex.html', {'current_pokemon': current_pokemon, 'pokemon_data': pokemon_data})

def team(request):
    pokemon_data = get_cached_pokemon_data()
    return render(request, 'team.html', {'pokemon_data': pokemon_data})


@sync_to_async
def get_pokemon_data_sync():
    return fetch_pokemon_data()

async def get_cached_pokemon_data():
    pokemon_data = cache.get('pokemon_data')
    if pokemon_data is None:
        # Assure-toi d'utiliser 'await' pour obtenir le résultat de la coroutine
        pokemon_data = await fetch_pokemon_data()
        # Maintenant que tu as les données, tu peux les mettre en cache
        cache.set('pokemon_data', pokemon_data, timeout=3600)
    return pokemon_data


