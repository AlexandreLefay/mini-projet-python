from django.core.cache import cache
from asgiref.sync import sync_to_async

from MonApplication.request.get_pokemon import get_pokemon_by_ids


# Permet de recuperer les données des Pokémon d'une équipe (nom, sprite, etc...)
def get_pokemon_data_team(team_id):
    teams  = cache.get('team_data')     # Récupérer les données de toutes les équipes en cache [{'id': 1, 'teamName': 'test', 'pokemon': [1, 2, 3]}, {'id': 2, 'teamName': 'test2', 'pokemon': [1, 2, 3]}]
    current_team = next((item for item in teams if item['id'] == team_id), None) # Les données de l'équipe actuelle {'id': 1, 'teamName': 'test', 'pokemon': [1, 2, 3]}
    team_pokemon_id = current_team['pokemon'] # Les IDs des Pokémon de l'équipe actuelle [1, 2, 3]

    pokemon_data = cache.get('pokemon_data') # Récupérer les données de tous les Pokémon en cache
    pokemon_data_team = get_pokemon_by_ids(pokemon_data, team_pokemon_id) # Récupérer les données des Pokémon de l'équipe actuelle
    return pokemon_data_team