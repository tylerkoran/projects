from cs50 import SQL
from helpers import fight

db = SQL("sqlite:///pokemon.db")

print("\n\n")

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