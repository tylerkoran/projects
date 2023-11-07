from cs50 import SQL
from helpers import fight

input("\nWELCOME TO THE PYTHON POKEMON TEXT GAME. YOUR GOAL IS TO BEAT THE OPPONENTS WITHOUT THE ABILITY TO RESTORE YOUR POKEMON THROUGH THE USE OF A POKEMON CENTER.")
input("\nCredit to, of course, Nintendo and Game Freak for the Pokemon games. Credit to pokemondb.net for information on different Pokemon, Pokemon moves, and information on the Pokemon world in general. Credit also to bulbapedia.bulbagarden.net for information on different Pokemon moves. Lastly, credit to Maija Haavisto of fiikus.net for the wonderful Ascii Art.")

db = SQL("sqlite:///pokemon.db")

yourPokemon = []
opponentPokemon = []
pokemon = db.execute("SELECT * FROM pokemon JOIN trainers ON trainerId = id")

''' saving Pokemon to yourPokemon and opponentPokemon lists '''
for individual in pokemon:
    if individual["trainer"] == "Ash":
        yourPokemon.append(individual)
        individual["move1PP"] = db.execute("SELECT pp FROM moves WHERE moveName = ?", individual["move1"])[0]["pp"]
        individual["move2PP"] = db.execute("SELECT pp FROM moves WHERE moveName = ?", individual["move2"])[0]["pp"]
        individual["move3PP"] = db.execute("SELECT pp FROM moves WHERE moveName = ?", individual["move3"])[0]["pp"]
        individual["move4PP"] = db.execute("SELECT pp FROM moves WHERE moveName = ?", individual["move4"])[0]["pp"]
    if individual["trainerId"] == db.execute("SELECT leaderId FROM places")[0]["leaderId"]:
        opponentPokemon.append(individual)

''' calling the fight function '''
if not fight(yourPokemon, opponentPokemon, 0):  # fight 1. "fight" returns true if the user wins the battle and false otherwise
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


opponentPokemon = []
for individual in pokemon:
    if individual["trainerId"] == db.execute("SELECT leaderId FROM places")[2]["leaderId"]:
        opponentPokemon.append(individual)

''' calling the fight function '''
if not fight(yourPokemon, opponentPokemon, 2):  # fight 3
    print("GAME OVER. Thanks for playing!")
    exit()


opponentPokemon = []
for individual in pokemon:
    if individual["trainerId"] == db.execute("SELECT leaderId FROM places")[3]["leaderId"]:
        opponentPokemon.append(individual)

''' calling the fight function '''
if not fight(yourPokemon, opponentPokemon, 3):  # fight 4
    print("GAME OVER. Thanks for playing!")
    exit()


print("YOU WIN!")  # only prints if all battles are won
exit()
