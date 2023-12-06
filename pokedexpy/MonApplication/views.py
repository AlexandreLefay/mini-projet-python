from django.http import HttpResponse
import requests

from django.shortcuts import render

def accueil(request):
    pokemon_list = get_pokemon_list()
    return render(request, 'pokemon_list.html', {'pokemon_list': pokemon_list })

def team(request):
    return render(request, 'team.html')

def get_pokemon_list():
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_list = []
        for pokemon in data["results"]:
            sprite = get_pokemon_sprite(pokemon["name"])
            stats = get_pokemon_stats(pokemon["name"])
            pokemon_list.append({
                "name": pokemon["name"],
                "sprite": sprite,
                "stats": stats
            })
        return pokemon_list
    else:
        return []

def get_pokemon_sprite(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["sprites"]["front_default"]
    else:
        return None

def get_pokemon_stats(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        stats = []
        for stat in data["stats"]:
            stats.append({
                "name": stat["stat"]["name"],
                "value": stat["base_stat"]
            })
        return stats
    else:
        return []
