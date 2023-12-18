from django.core.cache import cache

from MonApplication.request.get_pokemon import fetch_pokemon_data


# Fonction asynchrone pour obtenir les données Pokémon en cache
async def get_cached_pokemon_data():
    pokemon_data = cache.get('pokemon_data')
    if pokemon_data is None:
        pokemon_data = await fetch_pokemon_data()
        cache.set('pokemon_data', pokemon_data, timeout=3600)
    return pokemon_data

# Fonction asynchrone pour obtenir les données d'une équipe en cache
async def get_cached_team_data():
    team_data = cache.get('team_data')
    # print(team_data)
    if team_data is None:
        return []
    return team_data