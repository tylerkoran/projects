from random import randint
from cs50 import SQL
from asciiArt import asciiArt

db = SQL("sqlite:///pokemon.db")

placesAll = db.execute("SELECT * FROM places JOIN trainers ON id = leaderId")

def userNewPokemon(yourPokemon, place):
    ''' first checking if user has any more usable pokemon, then choosing pokemon and saving their moves to the pokemon moves list of dictionaries for user '''
    youLose = True
    for individual in yourPokemon:
        if individual["hp"] > 0:
            youLose = False
    if youLose:
        input("ASH is out of usable Pokemon. " + placesAll[place]["trainer"] + " wins!")
        youLosePhrase = db.execute("SELECT phraseLose FROM trainers WHERE id = 3")[0]["phraseLose"]
        input("ASH: \"" + youLosePhrase + "\"")
        input(placesAll[place]["trainer"] + ": \"" + placesAll[place]["phraseWin"]  + "\"")
        return False

    print("Your Pokemon:   ", end="")
    for individual in yourPokemon:
        if individual["hp"] > 0:
            print(individual["pokemonName"] + "    ", end="")
    print()
    usage = False
    while usage == False:
        choice = input("Which would you like to choose? > ")  # making sure you choose a Pokemon that you have
        for individual in yourPokemon:
            if choice == individual["pokemonName"] and individual["hp"] > 0:
                asciiArt(choice)
                yourCurrentPokemon = individual
                usage = True
                break

    yourCurrentPokemonMoves = [
        db.execute("SELECT * FROM moves WHERE moveName = ?", yourCurrentPokemon["move1"])[0],
        db.execute("SELECT * FROM moves WHERE moveName = ?", yourCurrentPokemon["move2"])[0],
        db.execute("SELECT * FROM moves WHERE moveName = ?", yourCurrentPokemon["move3"])[0],
        db.execute("SELECT * FROM moves WHERE moveName = ?", yourCurrentPokemon["move4"])[0]
    ]
    
    ''' printing choice '''
    input("ASH chooses " + yourCurrentPokemon["pokemonName"] + "!")
    input(yourCurrentPokemon["pokemonName"] + " has " + str(yourCurrentPokemon["hp"]) + " HP.")
    return yourCurrentPokemon, yourCurrentPokemonMoves

# function for opponent choosing new pokemon
def opponentNewPokemon(i, opponentPokemon, place):
    ''' checking if opponent has more usable Pokemon, otherwise showing that you win. If the opponent has usable Pokemon, setting the next one and saving their moves to the moves list'''
    try:
        opponentCurrentPokemon = opponentPokemon[i]
    except IndexError:
        input(placesAll[place]["trainer"] + " is out of usable Pokemon. ASH wins!")
        youWin = db.execute("SELECT phraseWin FROM trainers WHERE id = 3")[0]["phraseWin"]
        input("ASH: \"" + youWin + "\"")
        input(placesAll[place]["trainer"] + ": \"" + placesAll[place]["phraseLose"] + "\"")
        return False

    opponentCurrentPokemonMoves = [
        db.execute("SELECT * FROM moves WHERE moveName = ?", opponentCurrentPokemon["move1"])[0],
        db.execute("SELECT * FROM moves WHERE moveName = ?", opponentCurrentPokemon["move2"])[0],
        db.execute("SELECT * FROM moves WHERE moveName = ?", opponentCurrentPokemon["move3"])[0],
        db.execute("SELECT * FROM moves WHERE moveName = ?", opponentCurrentPokemon["move4"])[0]
    ]
    
    ''' printing choice and HP of both players' chosen Pokemon '''
    asciiArt(opponentCurrentPokemon["pokemonName"])
    input(placesAll[place]["trainer"] + " chooses " + opponentCurrentPokemon["pokemonName"] + "!")
    input(opponentCurrentPokemon["pokemonName"] + " has " + str(opponentCurrentPokemon["hp"]) + " HP.")
    return opponentCurrentPokemon, opponentCurrentPokemonMoves


def fight(yourPokemon, opponentPokemon, place):
    input("\n\n\nYou arrive at " + placesAll[place]["location"] + " and see " + placesAll[place]["description"] + " You walk inside and see someone standing in the entryway. \"Hello, my name is " + placesAll[place]["trainer"] + ". " + placesAll[place]["phrase1"] + "\"\n")

    ''' grab current user and opponent pokemon and moves '''
    user = userNewPokemon(yourPokemon, place)
    yourCurrentPokemon = user[0]
    yourCurrentPokemonMoves = user[1]

    i = 0
    opponent = opponentNewPokemon(i, opponentPokemon, place)
    opponentCurrentPokemon = opponent[0]
    opponentCurrentPokemonMoves = opponent[1]

    while True:
        ''' displaying moves and choosing '''
        print("\n" + "MOVES:   ")
        for move in yourCurrentPokemonMoves:
            print(move["moveName"], end="  ")
            print("PP: " + str(move["pp"]))
        print()

        usage = False
        while usage == False:
            choice = input("CHOOSE MOVE \n> ")
            for move in yourCurrentPokemonMoves:
                if choice == move["moveName"]:
                    if move["pp"] == 0:
                        input("Not enough PP to use that move.")
                    else:
                        choice = move
                        usage = True
                        break

        choice["pp"] -= 1
        input(yourCurrentPokemon["pokemonName"] + " uses " + choice["moveName"] + "!")


        ''' inflicting damage and checking if the opponent's pokemon fainted '''
        damage = int(choice["damage"] * yourCurrentPokemon["level"] / 20)
        input("It does " + str(damage) + " damage!\n")
        opponentCurrentPokemon["hp"] -= damage

        if opponentCurrentPokemon["hp"] < 1:
            input(opponentCurrentPokemon["pokemonName"] + " fainted!")
            i += 1
            opponent = opponentNewPokemon(i, opponentPokemon, place)
            if not opponent:
                return True
            opponentCurrentPokemon = opponent[0]
            opponentCurrentPokemonMoves = opponent[1]
        else:
            input(opponentCurrentPokemon["pokemonName"] + " has " + str(opponentCurrentPokemon["hp"]) + " HP.")


        ''' opponent chooses a move '''
        counter = 0
        while True:
            counter += 1
            choice = opponentCurrentPokemonMoves[randint(0, len(opponentCurrentPokemonMoves) - 1)] # depending on number of moves
            if choice["pp"] > 0:
                break
            if counter >= 1000:
                choice = {"moveName":"throw beans", "damage":3, "pp":1}
                break

        choice["pp"] -= 1
        input(opponentCurrentPokemon["pokemonName"] + " uses " + choice["moveName"] + "!")

        ''' inflicting damage and checking if user Pokemon fainted, then printing user current Pokemon HP '''
        damage = int(choice["damage"] * opponentCurrentPokemon["level"] / 20)
        input("It does " + str(damage) +  " damage!\n")
        yourCurrentPokemon["hp"] -= damage

        if yourCurrentPokemon["hp"] < 1:
            input(yourCurrentPokemon["pokemonName"] + " fainted!")
            user = userNewPokemon(yourPokemon, place)
            if not user:
                return False
            yourCurrentPokemon = user[0]
            yourCurrentPokemonMoves = user[1]
        else:
            input(yourCurrentPokemon["pokemonName"] + " has " + str(yourCurrentPokemon["hp"]) + " HP.")
