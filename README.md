# projects
This repository currently includes my unfinished CS50 final project, which is a text-based Pokemon game.

To view my project, start with main.py. This is where the flow of the game is stored. main.py pulls from functions in helpers.py. pokemon.db is the database where information is stored on the different Pokemon, attack moves, trainers, and places. A function in helpers.py also prints Ascii art provided in asciiArt.py.

My eventual goal is to make it so the user has to beat 4 opponents ("The Elite 4") without being able to regain health or PP through the use of a "Pokemon Center." At this point, I am aware of at least one bug: if you beat the first opponent, the power points (PP) of the Pokemon you were using resets when it should remain the same. I am also aware that there is not a whole lot of skill involved for the user at the moment, however I am going to try and include type advantages, so the user must be strategic in choosing which Pokemon to use as well as which moves to use. I would also like to give the user the option to switch out Pokemon and access a bag where they have some healing potions.

I am open to any and all feedback!
