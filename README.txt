Files included
--------------
-tournament_test.py:
	Test scripts validating each of the included modules.
-tournament.py:
	Tournament file where all the modules are defined.
-tournament.sql:
	PostgreSQL setup up file and table schema definition.


Requirements
----------------
-Python 2.7
-PostgreSQL Database

The tournament.py file requires the existance of the database tournament.


Swiss Tournament Pairings
-------------------------

The main file containing all the methods used to register players,find and arrange the swiss pairs is called "tournament.py". 

The file containing the database schema is called "tournament.sql"

The test suite where all test scripts for the project reside is called "tournament_test.py"


Setup
-----
Create the tournament database:
	-Access and pre-existing PostgreSQL database and run the setup file "tournament.sql"
	i.e. \i /file/path/to/tournament.py
	-The setup file will create and define the tables required for the tournament


Test Scripts
------------

The file "tournament_test.py" contains a series of test scripts that were used in order to properly create the program. When "tournament_test.py" runs it tests all the potential scenarios that are supposed to be successful and checks whether these passed or not. Note all functions contained in "tournament.py" successfully passed all the tests.

