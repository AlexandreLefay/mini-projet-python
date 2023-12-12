import aiohttp
import asyncio

# Définition d'une fonction asynchrone pour récupérer les données d'un Pokémon.
async def fetch_pokemon(session, url):
    # Exécution d'une requête GET asynchrone vers l'URL fournie.
    async with session.get(url) as response:
        # Attente de la réponse et conversion en JSON.
        return await response.json()

# Définition d'une fonction asynchrone pour récupérer les données de plusieurs Pokémon.
async def fetch_pokemon_data():
    # Création d'une session asynchrone. Cela permet de réutiliser des connexions pour de multiples requêtes.
    async with aiohttp.ClientSession() as session:
        pokemons = []  

        for i in range(1, 152):  
            
            url = f"https://pokeapi.co/api/v2/pokemon/{i}/"
            
            pokemon_data = await fetch_pokemon(session, url)

            # Extraction et stockage des informations spécifiques de chaque Pokémon.
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

        return pokemons

# Création d'une boucle d'événements pour exécuter des fonctions asynchrones.
loop = asyncio.get_event_loop()
# Exécution de la fonction `fetch_pokemon_data` et attente de son achèvement.
pokemons = loop.run_until_complete(fetch_pokemon_data())
# Affichage des données récupérées.
print(pokemons)
