from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import requests
from django.shortcuts import render
from django.core.cache import cache

def home(request):
    return render(request, 'home.html')

def pokedex(request):
    pokemon_data = get_cached_pokemon_data()
    return render(request, 'pokedex.html', {'pokemon_data': pokemon_data})

def team(request):
    pokemon_data = get_cached_pokemon_data()
    return render(request, 'team.html', {'pokemon_data': pokemon_data})


    """
je n'arrive toujours pas a regler le probleme de lenteur, get_cached_pokemon_data() permet de garde 
les informations en cache pour ne pas avoir a les recharger a chaque fois (pendant 1h) mais c'est toujours aussi lent, j'ai limité 
le nombre de pokemon a 12 pour avoir un exemple
    """
def get_cached_pokemon_data():
    pokemon_data = cache.get('pokemon_data')
    if pokemon_data is None:
        pokemon_data = fetch_pokemon_data()
        cache.set('pokemon_data', pokemon_data, timeout=3600)  # Cache data for 1 hour
    return pokemon_data

    """
On recupere les données de l'API pokemon
Il faut juste rajouter ce qu'il nous faut dans le dictionnaire pokemon
    """ 
def fetch_pokemon_data():
    response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=151')
    if response.status_code == 200:
        pokemons = {}
        data = response.json()
        for i in range(151):
            pokemons[i+1] = data["results"][i]["name"]
        #print(pokemons)
        pokemon_data = [{'name': pokemon['name'],
                        'id': i,
                        'sprite_front': f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{i}.png"}
                        for i, pokemon in enumerate(data['results'], start=1)]
        #print(pokemon_data)
        return pokemon_data
    else:
        return None
    
    # pokemon_data = []
    # for i in range(1, 151):
    #     response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}")
    #     if response.status_code == 200:
    #         data = response.json()
    #         pokemon = {
    #             'name': data['name'],
    #             'type': data['types'][0]['type']['name'],
    #             'attack': data['stats'][1]['base_stat'],
    #             'weight': data['weight'],
    #             'hp': data['stats'][0]['base_stat'],
    #             'sprite_front': data['sprites']['front_default'],
    #         }
    #         pokemon_data.append(pokemon)
    # return pokemon_data


def create_team(request):
    team = []
    for _ in range(6):
        # pokemon_id = generate a random Pokemon ID or get it from the user input
        pokemon_data = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}').json()
        team.append({
            'name': pokemon_data['name'],
            'types': [t['type']['name'] for t in pokemon_data['types']]
            # you can include more details as per your requirement
        })
    return JsonResponse({'team': team})