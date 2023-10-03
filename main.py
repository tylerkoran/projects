from cs50 import SQL
from helpers import fight

input("\nWELCOME TO THE POKEMON CHALLENGE. YOUR GOAL IS TO BEAT THE OPPONENTS WITHOUT THE ABILITY TO RESTORE YOUR POKEMON THROUGH THE USE OF A POKEMON CENTER.")
input("\nCredit to, of course, Nintendo and Game Freak for the Pokemon games. Credit to pokemondb.net for information on different Pokemon, Pokemon moves, and information on the Pokemon world in general. Credit also to bulbapedia.bulbagarden.net for information on different Pokemon moves. Lastly, credit to Maija Haavisto of fiikus.net for the wonderful Ascii Art.")

db = SQL("sqlite:///pokemon.db")

yourPokemon = []
opponentPokemon = []
pokemon = db.execute("SELECT * FROM pokemon")

''' saving Pokemon to yourPokemon and opponentPokemon lists '''
for individual in pokemon:
    if individual["trainerId"] == 3:
        yourPokemon.append(individual)
    if individual["trainerId"] == db.execute("SELECT leaderId FROM places")[0]["leaderId"]:
        opponentPokemon.append(individual)

''' calling the fight function '''
if not fight(yourPokemon, opponentPokemon, 0):  # fight 1
    print("GAME OVER. Thanks for playing!")
    exit()


''' saving new opponent Pokemon to opponentPokemon list'''
opponentPokemon = []
for individual in pokemon:
    if individual["trainerId"] == db.execute("SELECT leaderId FROM places")[1]["leaderId"]:
        opponentPokemon.append(individual)

''' calling the fight function '''
if not fight(yourPokemon, opponentPokemon, 1):  # fight 2
    print("GAME OVER. Thanks for playing!")
    exit()


print("YOU WIN!")
exit()
