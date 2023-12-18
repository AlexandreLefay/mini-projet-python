import asyncio
import json
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import requests
from django.core.cache import cache
from asgiref.sync import sync_to_async
from django.shortcuts import render

from MonApplication.request.get_pokemon import fetch_pokemon_data
from MonApplication.request.get_pokemon import get_pokemon_id_from_request
from MonApplication.request.get_pokemon import get_pokemon_by_ids
from MonApplication.request.get_pokemon import get_pokemon_by_id
from MonApplication.request.get_pokemon import filter_pokemon_by_query

from MonApplication.function.cache_data import get_cached_pokemon_data
from MonApplication.function.cache_data import get_cached_team_data

from MonApplication.function.manage_team import get_pokemon_data_team

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
    test = request.GET.get('team_id', 1)
    print(test)
    return render(request, 'team.html', {'team_data': team_data})


# Vue pour créer une équipe Pokémon
def create_team(request):
    if request.method == 'POST':
        teamName = request.POST.get('teamName')

        # Récupérer le tableau actuel du cache ou initialiser un nouveau tableau si aucun n'existe
        team_data = cache.get('team_data', [])

        # Récupérer l'ID actuel ou initialiser à 1 si aucun n'existe
        current_id = cache.get('current_team_id', 0)
        current_id += 1

        # Ajouter le nouveau teamName et l'ID au tableau
        team_data.append({'id': current_id, 'teamName': teamName, 'pokemon': []})

        # Mise à jour du cache avec le nouveau tableau et l'ID
        cache.set('team_data', team_data, timeout=3600)
        cache.set('current_team_id', current_id, timeout=3600)

        return render(request, 'create_team.html', {'teamName': teamName})
    else:
        return render(request, 'create_team.html')
    
# Vue pour afficher les détails d'une équipe
async def detail_team(request, team_id):        
    teams  = cache.get('team_data')     # Récupérer les données de toutes les équipes en cache [{'id': 1, 'teamName': 'test', 'pokemon': [1, 2, 3]}, {'id': 2, 'teamName': 'test2', 'pokemon': [1, 2, 3]}]
    current_team = next((item for item in teams if item['id'] == team_id), None) # Les données de l'équipe actuelle {'id': 1, 'teamName': 'test', 'pokemon': [1, 2, 3]}
    team_pokemon_id = current_team['pokemon'] # Les IDs des Pokémon de l'équipe actuelle [1, 2, 3]

    pokemon_data = await get_cached_pokemon_data() # Récupérer les données de tous les Pokémon en cache
    pokemon_data_team = get_pokemon_data_team(team_id) # Récupérer les données des Pokémon de l'équipe actuelle
    
    
    if request.method == 'POST':
        data = json.loads(request.body) 
        pokemonId = data.get('pokemonId') # Récupérer l'ID du Pokémon à ajouter à l'équipe

        team_pokemon_id.append(pokemonId) # Ajouter l'ID du Pokémon à la liste des IDs des Pokémon de l'équipe actuelle
        current_team['pokemon'] = team_pokemon_id  # Mise à jour de current_team
        cache.set('team_data', teams)  # Mise à jour du cache avec les nouvelles données

        pokemon_data_team = get_pokemon_by_ids(pokemon_data, team_pokemon_id) 
        return render(request, 'detail_team.html', {'team': current_team, 'pokemon_data': pokemon_data, 'pokemon_data_team': pokemon_data_team})
    else:
        return render(request, 'detail_team.html', {'team': current_team, 'pokemon_data': pokemon_data, 'pokemon_data_team': pokemon_data_team})

# Vue pour debug mes données en cache, accessible via l'URL /cache_data
def cache_data(request):
    team_data = cache.get('team_data')
    pokemon_data = cache.get('pokemon_data')
    return render(request, 'cache_data.html', {'team_data': team_data, 'pokemon_data': pokemon_data})



#Il faut revoir les fonctions dans l'application pour async await.
# Fonction synchrone pour obtenir les données Pokémon
@sync_to_async
def get_pokemon_data_sync():
    return fetch_pokemon_data()


