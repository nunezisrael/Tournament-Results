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
-Virtual Machine (Linux i.e. Ubuntu) with Vagrant configuration already pre-installed.

The tournament.py file requires the existence of the database tournament.


Swiss Tournament Pairings
-------------------------

The main file containing all the methods used to register players,find and arrange the swiss pairs is called "tournament.py". 

The file containing the database schema is called "tournament.sql"

The test suite where all test scripts for the project reside is called "tournament_test.py"


Test Scripts
------------

The file "tournament_test.py" contains a series of test scripts that were used in order to properly create the program. When "tournament_test.py" runs it tests all the potential scenarios that are supposed to be successful and checks whether these passed or not. Note all functions contained in "tournament.py" successfully passed all the tests.


Setup
-----
1. Access the virtual machine through CLI (command prompt or terminal) and browser to the vagrant folder.
	i.e. “vagrant up” (to start the virtual machine) and “vagrant ssh” (to connect to 	the machine)
2. Create the tournament database:
	-Access the pre-existing PostgreSQL database and run the setup file "tournament.sql”.
	HINT: you can connect to any existing database, (\c forum) where forum is a pre-existing database, and there run the setup file.
	i.e. \i /vagrant/tournament/tournament.sql
	-The setup file will create and define the tables required for the tournament
3. Run another instance of the virtual machine on a separate command prompt or terminal (i.e. vagrant ssh) and run the test scripts.
	i.e python tournament_test.py

4. Done. All test will be passes and “success!” will print out.


