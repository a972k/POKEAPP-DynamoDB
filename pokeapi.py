import requests
# api url to fetch all pokemon names
pokeapi_url = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"

# functions to interact with the PokeAPI fetch data and confirm successful retrieval
def fetch_all_pokemon_names():
    response = requests.get(pokeapi_url)
    if response.status_code == 200:
        results = response.json()['results']
        return [p['name'] for p in results]
    else:
        print("Failed to get Pokémon list.")
        return []

# function to fetch details of a specific Pokémon by name and confirm successful retrieval
def fetch_pokemon_details(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data["name"],
            "base_experience": data["base_experience"],
            "abilities": [a["ability"]["name"] for a in data["abilities"]]
        }
    return None
