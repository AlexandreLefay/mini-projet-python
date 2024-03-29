import asyncio
import aiohttp
import requests

# Constantes
POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon/"
POKEMON_COUNT = 151  # Nombre total de Pokémon à récupérer (première génération)
CACHE_TIMEOUT = 3600  # Durée de vie du cache en secondes


# Fonction pour récupérer les données Pokémon (un ou tous).
async def get_pokemon_data(pokemon_id=None):
    async with aiohttp.ClientSession() as session:
        if pokemon_id:
            return await fetch_pokemon(session, f"{POKEMON_API_URL}{pokemon_id}/")
        else:
            return await fetch_multiple_pokemons(session)


# Fonction pour récupérer les données d'un Pokémon spécifique.
async def fetch_pokemon(session, url):
    try:
        async with session.get(url) as response:
            return await response.json()
    except aiohttp.ClientResponseError as e:
        return {'error': str(e), 'message': 'Failed to fetch pokemon data.'}


# Fonction pour récupérer les données de plusieurs Pokémon en parallèle.
async def fetch_multiple_pokemons(session):
    tasks = [fetch_pokemon(session, f"{POKEMON_API_URL}{i}/") for i in range(1, POKEMON_COUNT + 1)]
    responses = await asyncio.gather(*tasks)
    return [extract_pokemon_info(pokemon_data) for pokemon_data in responses if 'name' in pokemon_data]


# Extrait les informations pertinentes d'un Pokémon.
def extract_pokemon_info(pokemon_data):
    return {
        'name': pokemon_data['name'],
        'sprite_front': pokemon_data['sprites']['front_default'],
        'sprite_back': pokemon_data['sprites']['back_default'],
        'id': pokemon_data['id'],
        'types': [t['type']['name'] for t in pokemon_data['types']],
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight'],
        'hp': pokemon_data['stats'][0]['base_stat'],
        'moves': [move['move']['name'] for move in pokemon_data['moves']]
    }

# Récupération de la description du pokemon par son id.
async def get_pokemon_description(pokemon_id):
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_id}/"

    async with aiohttp.ClientSession() as session:
        async with session.get(species_url) as response:
            if response.status != 200:
                return "Erreur lors de la récupération des données de l'espèce du Pokémon."

            species_data = await response.json()

            # Recherche de la description en français
            for flavor_text_entry in species_data['flavor_text_entries']:
                if flavor_text_entry['language']['name'] == 'fr':
                    return flavor_text_entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')

            return "Description en français non trouvée."
