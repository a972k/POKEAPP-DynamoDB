# define pokemon data display function
def display_pokemon(pokemon):
    print("\npokemon drawn ")
    print(f"name: {pokemon['name'].title()}")
    print(f"base experience: {pokemon['base_experience']}")
    print(f"abilities: {', '.join(pokemon['abilities'])}")
    print("\n")
