#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def DB(QUERY, arg1, arg2, result):
    """Connects to the PostgreSQL database and executes the query
    QUERY - the actual query executed on the DB
    arg1 - optional value executed with the QUERY.
    Avoids injection attacks.
    arg2 - optional value executed with the QUERY and arg1.
    Avoids injection attacks.
    result - if value is set to 'None' no rows are returned.
    Otherwise all rows are returned."""

    conn = psycopg2.connect(database="tournament")
    c = conn.cursor()
    # executes query without any optional parameter
    if (arg1, arg2) == None:
        c.execute(QUERY)
    # executes query with arg1 set to a value and avoids injection attacks
    elif (arg2) == None:
        c.execute(QUERY, (arg1, ))
    # executes the query with both optinal parameters and avoids
    # injection attacks
    else:
        c.execute(QUERY, (arg1, arg2, ))
    conn.commit()
    # if the result the rows are fetched
    while True:
        if (result) == None:
            break
        else:
            result = c.fetchall()
            return result
            break
    conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    DB('delete from standings', None, None, None)


def deletePlayers():
    """Remove all the player records from the database."""

    DB('delete from standings', None, None, None)


def countPlayers():
    """Returns the number of players currently registered."""

    total_players = DB('select count(player_id) from standings', None, None, 1)

    return total_players[0][0]


def registerPlayer(fullname):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.
    Args:
        name: the player's full name (need not be unique).
    """
    playerID = DB('''insert into standings (fullname) values (%s)
        returning player_id''', fullname, None, 1)
    # Also inserting players into the byestatus table
    DB('''insert into byestatus (player_id) values (%s)''',
        playerID[0][0], None, None)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # returning the list of players and their standings
    standings = DB('select * from standings order by wins desc', None, None, 1)
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # updating the winner record for every round
    DB('''update standings set wins = wins + 1, matches = matches + 1 where
        player_id = %s''', winner, None, None)

    # updating the loser record for every round
    DB('''update standings set matches = matches + 1 where player_id = %s''',
        loser, None, None)


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # Getting a list of players and their standings
    player_list = playerStandings()
    swiss_pairs = []
    # making the SQL list and making pairs
    for i in range(0, countPlayers(), 2):
        pair = (player_list[i][0], player_list[i][1], player_list[i+1][0],
                player_list[i+1][1])
        swiss_pairs.append(pair)
    return swiss_pairs
