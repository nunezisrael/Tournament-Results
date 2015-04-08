Swiss Tournament Pairings

The main file is called "tournament.py". The following functions are within this file and their usage.


connect():
Creates a connection to the DB and make it available for any other function.

deleteMatches():
Deletes all records from the matches table and resets the match sequence. This function is used to remove all match information when a new tournament is started.

deletePlayers():
Deletes all records from the players table. This function is used to remove all the player information when a new tournament is started.


countPlayers():
Provides a count of all players registered for the tournament. Used to determined how many rounds should be played until a winner is determined.


registerPlayer(fullname):
Allows players to be registered into the tournament and populated those tables where a player record is needed/referenced.


playerStandings():
Provides a list of player status: wins and matches. This list is used to create the swiss pairs needed for the subsequent rounds.


reportMatch(winner,loser):
