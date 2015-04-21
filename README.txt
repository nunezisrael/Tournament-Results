Swiss Tournament Pairings
-------------------------

The main file contaning all the methods used to find and arrange the swiss pairs, this is called "tournament.py". 

The main file containning the database schema is called "tournament.sql"

The file were an actual tournament is played is called, "game.py"

The test suite where all test scripts for the project reside is called "tournament_test.py"

Functions
---------
The following functions are within the file "tournament.py" and their usage.

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
Provides a list of player current status: wins and matches. This list is used to create the swiss pairs needed for the subsequent rounds; initialy before any match is played and every time after a match is played.

reportMatch(winner,loser):
Function takes two parameters: the first parameter is the winner of the match, the second parameter is the loser of the match. The function will increase the "wins" and "matches" by one for the winner and only increase the "matches" for the loser. This function is used to report the winner and loser of every match played.

swissPairings():
Function makes use of the playerStandings() method to pair up players next with similar win records. When there is an odd number of players the function will give a "bye" (a win) to the player with the least wins. The function will also check to ensure that no player receives two "byes".

Data Base Schema
----------------

The file "tournament.sql" containts the following tables and their definitions:

Players - stores players registered for the tournament
Matches - stores match played between two players
playerStandings - keeps track of the current standings of each player per match
bye - keeps track of the "bye" each player has received.

Game environment
----------------

The file "game.py" creates an enviroment for the tournament to be played and makes use of all the functions in "tournament.py" and all the tables on "tournament.sql". The program takes in the several inputs for the user to run the tournament.

-When the program is ran, it first asks if the data from previous tournaments should be deleted or not.
-Next the program will ask to enter the number of new players to be added to the tournament, this number is used to prompt the user to enter each player one-at-a-time.

Once all the players are entered the total number of players registers is obtained and used to determine how many rounds should be played until a winner is determined.

After each round is played the program will output the swiss pairings created and the match winner per match. Once the entire tournament runs the program also indicates the winner of the tournament, whom corresponds to the player with the most "wins."

********************************************************************************************
Note the program does not validate user input, i.e. if it asks for number and a character is entered the error thrown is not handled.
********************************************************************************************

HOW TO RUN THE TOURNAMENT:

1. Run script game.py
2. User will be prompted with the following question:
"Do you want clear previous tournament history?"
If "Y" is entered then ALL table data deleted i.e. all tables are wiped.
If "N" is entered ALL table date is preserved and the tournament will be ran with the "OLD DATA" + the "NEW DATA" i.e. if a tournament with 2 players was ran before and the tables are not wiped ("N"), if another player is entered then the tournament will be ran with 3 players.
3. User will be prompted to, "enter the number of players into the tournament". Depending the on the option selected on step #2, the total number of players register will be ALL previously registered players + any new players entered OR only the newly registered players. The total rounds to be played will be based on the number of total players registered.
4. The tournament begins:	
4.1 The current standings of all players is printed to the screen.
4.2 The swiss pairs created (based on the standings step 4.1) face off i.e the match is played. The winner per match is played and the winner recorded.
4.3 Steps 4.1 and 4.2 are repeated per round until a winner is found.
5. The tournament winner is printed.

Test Scripts
------------

The file "tournament_test.py" contains a series of test scripts that were used in order to create the program. When "tournament_test.py" runs it tests all the functions contained in "tournament.py" and successfully passes all the tests.