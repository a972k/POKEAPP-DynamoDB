import random
from storage import get_pokemon, save_pokemon
from pokeapi import fetch_all_pokemon_names, fetch_pokemon_details
from display import display_pokemon

# pokemon drawing game that uses PokeAPI + DynamoDB
def main():
    print("Welcome to the Pokémon Drawing Game!")

    # main game loop
    while True:
        choice = input("Would you like to draw a Pokémon? (yes/no): ").strip().lower()

        if choice == "yes":
            all_names = fetch_all_pokemon_names()
            if not all_names:
                print("Failed to fetch Pokémon list. Try again.")
                continue

            selected = random.choice(all_names)
            pokemon_data = get_pokemon(selected)

            if pokemon_data:
                print("Pokémon already in database.")
                display_pokemon(pokemon_data)
            else:
                print("Fetching new Pokémon data...")
                details = fetch_pokemon_details(selected)
                if details:
                    save_pokemon(details)
                    display_pokemon(details)
                else:
                    print("Failed to fetch Pokémon details.")
        
        elif choice == "no":
            print("See you next time.")
            break

        else:
            print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()

