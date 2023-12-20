from random import uniform

from MonApplication.function.cache_data import get_cached_pokemon_data
from MonApplication.function.cache_data import get_cached_team_data
from MonApplication.function.filter import filter_pokemon_by_ids
from MonApplication.function.filter import filter_pokemon_by_query
from django.core.cache import cache
from django.shortcuts import render, redirect

# Constantes
POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_COUNT = 151  # Nombre total de Pokémon à récupérer (première génération)
CACHE_TIMEOUT = 3600  # Durée de vie du cache en secondes


# Vue pour la page d'accueil
def home(request):
    return render(request, 'home.html')


# Vue asynchrone pour afficher les données du Pokédex.
async def pokedex(request):
    pokemon_data = await get_cached_pokemon_data()
    pokemon_id = request.GET.get('pokemon_id', 1)
    current_pokemon = next((pokemon for pokemon in pokemon_data if pokemon['id'] == int(pokemon_id)), pokemon_data[0])
    pokemon_data = filter_pokemon_by_query(pokemon_data, request)
    return render(request, 'pokedex.html', {'current_pokemon': current_pokemon, 'pokemon_data': pokemon_data})


# Vue pour afficher nos équipes Pokémon
async def team(request):
    team_data = await get_cached_team_data()
    pokemon_data = await get_cached_pokemon_data()

    # Gestion de la soumission du formulaire pour créer une nouvelle équipe
    if request.method == 'POST':
        team_name = request.POST.get('teamName')
        if team_name and not any(team['teamName'] == team_name for team in team_data):
            current_id = cache.get('current_team_id', 0) + 1
            background_number = round(uniform(1, 8))
            team_data.append({
                'id': current_id,
                'teamName': team_name,
                'pokemon': [],  # Ajout d'un Pokémon par défaut
                'background': f"background_{background_number}.svg"
            })
            cache.set('team_data', team_data, timeout=CACHE_TIMEOUT)
            cache.set('current_team_id', current_id, timeout=CACHE_TIMEOUT)

    # Gestion de la suppression d'une équipe
    elif request.method == 'GET' and 'team_id' in request.GET:
        delete_team_id = int(request.GET['team_id'])
        team_data = [team for team in team_data if team['id'] != delete_team_id]
        cache.set('team_data', team_data, timeout=CACHE_TIMEOUT)

    return render(request, 'team.html', {'team_data': team_data, 'pokemon_data': pokemon_data})


# Vue pour afficher les détails d'une équipe
def handle_post_request(request, current_team):
    pokemon_id = request.POST.get('pokemon_id')
    if not (pokemon_id and pokemon_id.isdigit()):
        return

    pokemon_id = int(pokemon_id)
    if pokemon_id in current_team['pokemon']:
        current_team['pokemon'].remove(pokemon_id)
    elif len(current_team['pokemon']) < 6:
        current_team['pokemon'].append(pokemon_id)


def handle_get_request(request, current_team, pokemon_data):
    pokemon_id = request.GET.get('pokemon_id')
    if not (pokemon_id and pokemon_id.isdigit()):
        return

    pokemon_id = int(pokemon_id)
    if pokemon_id not in current_team['pokemon'] and len(current_team['pokemon']) < 6:
        if any(pokemon['id'] == pokemon_id for pokemon in pokemon_data):
            current_team['pokemon'].append(pokemon_id)
    elif pokemon_id in current_team['pokemon']:
        current_team['pokemon'].remove(pokemon_id)


# Vue pour afficher les détails d'une équipe
async def detail_team(request, team_id):
    teams = cache.get('team_data')
    current_team = next((team for team in teams if team['id'] == team_id), None)
    if not current_team:
        return redirect('home')  # Rediriger si l'équipe n'existe pas

    pokemon_data = await get_cached_pokemon_data()

    if request.method == 'POST':
        handle_post_request(request, current_team)
    elif request.method == 'GET':
        handle_get_request(request, current_team, pokemon_data)

    cache.set('team_data', teams)
    pokemon_data_team = filter_pokemon_by_ids(pokemon_data, current_team['pokemon'])
    return render(request, 'detail_team.html',
                  {'team': current_team, 'pokemon_data': pokemon_data, 'pokemon_data_team': pokemon_data_team})


# Vue pour debug les données en cache, accessible via l'URL /cache_data
def cache_data(request):
    team_data = cache.get('team_data')
    pokemon_data = cache.get('pokemon_data')
    return render(request, 'cache_data.html', {'team_data': team_data, 'pokemon_data': pokemon_data})
