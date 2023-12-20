from django.core.cache import cache

from MonApplication.request.get_pokemon import get_pokemon_data

CACHE_TIMEOUT = 3600  # Durée de vie du cache en secondes


# Fonction asynchrone pour obtenir les données Pokémon en cache.
async def get_cached_pokemon_data():
    pokemon_data = cache.get('pokemon_data')
    if pokemon_data is None:
        pokemon_data = await get_pokemon_data()
        cache.set('pokemon_data', pokemon_data, timeout=CACHE_TIMEOUT)
    return pokemon_data


# Fonction asynchrone pour obtenir les données d'une équipe en cache
async def get_cached_team_data():
    team_data = cache.get('team_data')
    if team_data is None:
        team_data = []
        cache.set('team_data', team_data, timeout=CACHE_TIMEOUT)
    return team_data
