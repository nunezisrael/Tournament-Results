#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def DB(QUERY, arg1, arg2, result):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = psycopg2.connect(database="tournament")# creating a connection
    c = conn.cursor()
    if arg1 == None and arg2 == None:
        c.execute(QUERY)
    elif arg2 == None:
        c.execute(QUERY,(arg1, ))
    else:
        c.execute(QUERY,(arg1,arg2))
    conn.commit()
    while True:
        if result == None:
            break
        else:
            result = c.fetchall()
            return result
            break
    conn.close()

def deleteMatches():
    """Remove all the match records from the database."""
    DB('delete from matches',None,None,None)

    #resetting the match number sequence upon deletion
    DB('alter sequence  matches_matchnumber_seq  restart with 1',None,None,None)


def deletePlayers():
    """Remove all the player records from the database."""
    DB('delete from players',None,None,None)
    DB('delete from playerstandings',None,None,None)


def countPlayers():
    """Returns the number of players currently registered."""

    total_players = DB('select count(id) from players',None,None,1)
    return total_players[0][0]


def registerPlayer(fullname):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    playerID = DB('insert into players (fullname) values (%s) returning id',fullname,None,1)

    #Also inserting the players into the playerstandings table without wins or matches
    DB("insert into playerstandings (playerid) values (%s)",playerID[0][0],None, None)

    #Also inserting players into the byestatus table
    DB("insert into byestatus (playerid) values (%s)",playerID[0][0],None, None)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.
    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    #returning the list of players and their standings    
    standings = DB('select * from pairs;',None,None,1)
    return standings

def reportMatch(winner,loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    #updating winner's record
    DB('update playerstandings set wins = wins + 1, matches = matches + 1 where playerid = (%s)',winner,None,None)

    #updating loser's record
    DB('update playerstandings set matches = matches + 1 where playerid = (%s)',loser,None,None)


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
    #Getting a list of players and their standings
    ps = playerStandings()
    total_players = countPlayers()

    if total_players % 2 == 0:
        swiss_pairs = []
        #pairing up players with similar standings
        for i in range(0,total_players,2):
            #recording into matches with swiss pairs
            match = (ps[i][0],ps[i][1],ps[i+1][0],ps[i+1][1])

            #inserting into matches table
            DB('insert into matches (firstplayerid,secondplayerid) values (%s,%s)',match[0],match[2],None)
            swiss_pairs.append(match) #adding the pairs to the list
            
        return swiss_pairs

    else:
        #when there are an odd number of players, finding one without a bye.
        bye_player = DB('select * from byeplayer',None,None,1)

        bye_player = bye_player[0]

        #Inserting the bye into the playerStandings and byestatus table 
        if bye_player == (None):

            winner = DB('''
            select *
            from playerstandings as ps join players as p
            on ps.playerid = p.id
            order by ps.wins
            ''',None,None,1)
            
            winner = winner[0][1]
        else:
            DB('update byestatus set bye = bye + 1 where playerid = (%s)',bye_player[0],None,None)
            
            DB('update playerstandings set wins = wins + 1, matches = matches + 1 where playerid = (%s)',bye_player[0],None,None)
            
            #removing the bye player from the list
            ps.pop(ps.index(bye_player))
            swiss_pairs = []

            #pairing up players with similar standings
            for i in range(0,len(ps),2):
                #recording into matches with swiss pairs
                match = (ps[i][0],ps[i][1],ps[i+1][0],ps[i+1][1]) 

                #inserting swiss pair into matches table
                DB('insert into matches (firstplayerid,secondplayerid) values (%s,%s)',match[0],match[2],None)

                swiss_pairs.append(match) #adding the pairs to the list
            return swiss_pairs
