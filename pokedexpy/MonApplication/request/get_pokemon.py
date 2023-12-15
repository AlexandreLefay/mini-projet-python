import aiohttp

# Définition d'une fonction asynchrone pour récupérer les données d'un Pokémon.
async def fetch_pokemon(session, url):
    # Exécution d'une requête GET asynchrone vers l'URL fournie.
    async with session.get(url) as response:
        # Attente de la réponse et conversion en JSON.
        return await response.json()

async def fetch_pokemon_data(pokemon_id=None):
    async with aiohttp.ClientSession() as session:
        if pokemon_id:
            # Construire l'URL pour un seul Pokémon.
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/"
            try:
                return await fetch_pokemon(session, url)
            except aiohttp.ClientResponseError as e:
                # Gérer l'erreur (par exemple, Pokémon non trouvé).
                return {'error': str(e), 'message': 'Failed to fetch pokemon data.'}
        else:
            # Récupérer les données pour une plage de Pokémon.
            pokemons = []
            for i in range(1, 152):  # 151 est le nombre de Pokémon de la première génération.
                url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
                try:
                    pokemon_data = await fetch_pokemon(session, url)
                    pokemon_info = {
                        'name': pokemon_data['name'],
                        'sprite_front': pokemon_data['sprites']['front_default'],
                        'sprite_back': pokemon_data['sprites']['back_default'],
                        'id': pokemon_data['id'],
                        'types': [t['type']['name'] for t in pokemon_data['types']],
                        'height': pokemon_data['height'],
                        'hp': pokemon_data['stats'][0]['base_stat'],
                        'moves': [move['move']['name'] for move in pokemon_data['moves']]
                    }
                    pokemons.append(pokemon_info)
                except aiohttp.ClientResponseError:
                    # Si un Pokémon spécifique ne peut être récupéré, on continue avec les suivants.
                    continue
            return pokemons
