import asyncio
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import requests
from django.core.cache import cache
from asgiref.sync import sync_to_async
from django.shortcuts import render

from MonApplication.request.get_pokemon import fetch_pokemon_data
from MonApplication.request.get_pokemon import get_pokemon_id_from_request
from MonApplication.request.get_pokemon import get_pokemon_by_id
from MonApplication.request.get_pokemon import filter_pokemon_by_query

from MonApplication.function.cache_data import get_cached_pokemon_data
from MonApplication.function.cache_data import get_cached_team_data

# Vue principale qui affiche la page d'accueil
def home(request):
    return render(request, 'home.html')

# Vue asynchrone pour afficher les données du Pokédex 
async def pokedex(request):
    pokemon_data = await get_cached_pokemon_data()
    pokemon_id = get_pokemon_id_from_request(request)
    current_pokemon = get_pokemon_by_id(pokemon_data, pokemon_id)
    pokemon_data = filter_pokemon_by_query(pokemon_data, request)

    return render(request, 'pokedex.html', {'current_pokemon': current_pokemon, 'pokemon_data': pokemon_data})

# Vue pour afficher nos équipes Pokémon
async def team(request):
    team_data = await get_cached_team_data()
    return render(request, 'team.html', {'team_data': team_data})


# Vue pour créer une équipe Pokémon
def create_team(request):
    if request.method == 'POST':
        teamName = request.POST.get('teamName')

        # Récupérer le tableau actuel du cache ou initialiser un nouveau tableau si aucun n'existe
        team_data = cache.get('team_data', [])

        # Ajouter le nouveau teamName au tableau
        team_data.append({'teamName': teamName})

        # Mise à jour du cache avec le nouveau tableau
        cache.set('team_data', team_data, timeout=3600)

        return render(request, 'create_team.html', {'teamName': teamName})
    else:
        return render(request, 'create_team.html')
    
# Vue pour debug mes données en cache, accessible via l'URL /cache_data
def cache_data(request):
    team_data = cache.get('team_data')
    pokemon_data = cache.get('pokemon_data')
    # print(team_data)
    # print(pokemon_data)
    return render(request, 'cache_data.html', {'team_data': team_data, 'pokemon_data': pokemon_data})

# Fonction synchrone pour obtenir les données Pokémon
@sync_to_async
def get_pokemon_data_sync():
    return fetch_pokemon_data()


