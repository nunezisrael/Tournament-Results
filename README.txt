Swiss Tournament Pairings
-------------------------

The main file containing all the methods used to find and arrange the swiss pairs, this is called "tournament.py". 

The main file containing the database schema is called "tournament.sql"

The file were an actual tournament is played is called, "game.py"

The test suite where all test scripts for the project reside is called "tournament_test.py"

REQUIRED MODULES
----------------
-Postgresql => psycopg2
-math
-bleach
-tournament

*All modules are already imported within game.py and tournament.py

********************************************************************************************
Note the program does not validate user input, i.e. if it asks for number and a character is entered the error thrown is not handled.
********************************************************************************************

HOW TO RUN THE TOURNAMENT:

Run and connect to the virtual machine :
A. vagrant up -> vagrant ssh -> psql -> \i /path to/tournament.sql 
B. vagrant up -> vagrant ssh -> python tournament.py

execute the script:
1. Run script game.py
2. User will be prompted with the following question:
"Do you want clear previous tournament history?"
If "Y" is entered then ALL table data deleted and delete is “cascaded” on dependent tables  i.e. all tables are wiped.
If "N" is entered ALL table date is preserved and the tournament will be ran with the "OLD DATA" + the "NEW DATA" i.e. if a tournament with 2 players was ran before and the tables are not wiped ("N"), if another player is entered then the tournament will be ran with 3 players.
3. User will be prompted to, "enter the number of players into the tournament". Depending the on the option selected on step #2, the total number of players register will be ALL previously registered players + any new players entered OR only the newly registered players. The total rounds to be played will be based on the number of total players registered.
4. The tournament begins:	
4.1 The current standings of all players is printed to the screen.
4.2 The swiss pairs created (based on the standings step 4.1) face off i.e the match is played. The winner per match is played and the winner recorded.
4.3 Steps 4.1 and 4.2 are repeated per round until a winner is found.
5. The tournament winner is printed.

Test Scripts
------------

The file "tournament_test.py" contains a series of test scripts that were used in order to properly create the program. When "tournament_test.py" runs it tests all the potential scenarios that are supposed to be successful and checks whether these passed or not.functions contained in "tournament.py" and successfully passes all the tests.

