import asyncio
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import requests
from django.core.cache import cache
from asgiref.sync import sync_to_async
from django.shortcuts import render
from MonApplication.request.get_pokemon import fetch_pokemon_data

# Vue principale qui affiche la page d'accueil
def home(request):
    return render(request, 'home.html')


# Vue pour afficher les données en cache
def afficher_donnees_cache(request):
    cached_data = cache.get('team_data')
    context = {'cached_data': cached_data}
    return render(request, 'cache_info.html', context)


# Vue asynchrone pour afficher les données du Pokédex
async def pokedex(request):
    # Récupération des données Pokémon en cache ou depuis la source
    pokemon_data = await get_cached_pokemon_data()

    # Récupère l'ID du Pokémon à partir de la requête GET
    pokemon_id = request.GET.get('pokemon_id', 1)
    # Trouve le Pokémon correspondant ou renvoie le premier par défaut
    current_pokemon = next((pokemon for pokemon in pokemon_data if pokemon['id'] == int(pokemon_id)), pokemon_data[0])

    # Recherche par nom de Pokémon si un terme de recherche est fourni
    query = request.GET.get('search', '')
    if query:
        pokemon_data = [pokemon for pokemon in pokemon_data if query.lower() in pokemon['name'].lower()]

    return render(request, 'pokedex.html', {'current_pokemon': current_pokemon, 'pokemon_data': pokemon_data})


# Vue pour afficher l'équipe Pokémon
def team(request):
    pokemon_data = get_cached_pokemon_data()
    return render(request, 'team.html', {'pokemon_data': pokemon_data})


# Vue pour créer une équipe Pokémon
def create_team(request):
    if request.method == 'POST':
        teamName = request.POST.get('teamName')
        team_data = get_cached_team_data(teamName)
        return render(request, 'create_team.html', {'teamName': teamName})
    else:
        team_data = cache.get('team_data')
        if team_data is not None:
            teamName = team_data.get('teamName')
            return render(request, 'create_team.html', {'teamName': teamName})
        else:
            return render(request, 'create_team.html')


# Fonction synchrone pour obtenir les données Pokémon
@sync_to_async
def get_pokemon_data_sync():
    return fetch_pokemon_data()


# Fonction asynchrone pour obtenir les données d'une équipe en cache
async def get_cached_team_data(teamData):
    team_data = cache.get('team_data')
    if team_data is None:
        cache.set('team_data', teamData, timeout=3600)
    return team_data


# Fonction asynchrone pour obtenir les données Pokémon en cache
async def get_cached_pokemon_data():
    pokemon_data = cache.get('pokemon_data')
    if pokemon_data is None:
        pokemon_data = await fetch_pokemon_data()
        cache.set('pokemon_data', pokemon_data, timeout=3600)
    return pokemon_data
