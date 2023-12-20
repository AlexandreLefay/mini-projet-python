# Fonction pour filtrer les Pokémon en fonction d'une requête.
def filter_pokemon_by_query(pokemon_data, request):
    query = request.GET.get('search', '').lower()
    return [pokemon for pokemon in pokemon_data if query in pokemon['name'].lower()]


# Fonction pour filtrer les données de Pokémon par leurs IDs.
def filter_pokemon_by_ids(pokemon_data, pokemon_ids):
    pokemon_ids = [int(p_id) for p_id in pokemon_ids]
    return [pokemon for pokemon in pokemon_data if pokemon['id'] in pokemon_ids]
