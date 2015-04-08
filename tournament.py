#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = psycopg2.connect(database="tournament")# creating a connection
    return conn


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    QUERY = "delete from matches"
    c.execute(QUERY)
    db.commit()

    #resetting the match number sequence upon deletion
    QUERY = "alter sequence  matches_matchnumber_seq  restart with 1"
    c.execute(QUERY)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    QUERY = "delete from players"
    c.execute(QUERY)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db  = connect()
    c = db.cursor()
    QUERY = "select count(id) from players"
    c.execute(QUERY)
    total_players = c.fetchall()
    db.close()
    return total_players[0][0]


def registerPlayer(fullname):
    """Adds a player to the tournament database.
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    QUERY = "insert into players (fullname) values (%s) returning id"
    c.execute(QUERY,(fullname, ))
    db.commit()
    playerID = c.fetchone()[0]

    #Also inserting the players into the playerstandings table without wins or matches
    QUERY = "insert into playerstandings (playerid) values (%s)"
    c.execute(QUERY,(playerID, ))
    db.commit()

    #Also inserting players into the byestatus table
    QUERY = "insert into byestatus (playerid) values (%s)"
    c.execute(QUERY,(playerID, ))
    db.commit()
    db.close()


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
    db = connect()
    c = db.cursor()

    #returning the list of players and their standings    
    QUERY = '''
    select p.id,p.fullname,s.wins, s.matches
    from players as p join playerstandings as s
    on p.id = s.playerid
    order by s.wins desc,s.matches
    '''
    c.execute(QUERY)
    standings = c.fetchall()
    db.close()
    return standings

def reportMatch(winner,loser):
    """Records the outcome of a single match between two players.
    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()

    #updating winner's record
    winner_QUERY = "update playerstandings set wins = wins + 1, matches = matches + 1 where playerid = (%s)"
    c.execute(winner_QUERY,(winner, ))
    db.commit()

    #updating loser's record
    loser_QUERY = "update playerstandings set matches = matches + 1 where playerid = (%s)"
    c.execute(loser_QUERY,(loser, ))
    db.commit()
    db.close()


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
    db = connect()
    c = db.cursor()
    
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
            QUERY = "insert into matches (firstplayerid,secondplayerid) values (%s,%s)"
            c.execute(QUERY,(match[0],match[2]))
            db.commit()

            swiss_pairs.append(match) #adding the pairs to the list
        db.close()
        return swiss_pairs

    else:
        #when there are an odd number of players, finding one without a bye.
        QUERY = '''
        select p.playerid, pl.fullname, p.wins, p.matches
        from byestatus as b join playerstandings as p
        on b.playerid = p.playerid join players as pl
        on pl.id = p.playerid
        where b.bye = 0
        order by p.wins, b.bye desc 
        '''
        c.execute(QUERY)
        bye_player = c.fetchone()

        #Inserting the bye into the playerStandings and byestatus table 
        if bye_player == (None):
            QUERY = "select * from playerstandings as ps join players as p on ps.playerid = p.id order by ps.wins"
            c.execute(QUERY)
            winner = c.fetchone()[1]
        else:
            QUERY = "update byestatus set bye = bye + 1 where playerid = (%s)"
            c.execute(QUERY,(bye_player[0], ))
            db.commit()
            QUERY = "update playerstandings set wins = wins + 1, matches = matches + 1 where playerid = (%s)"
            c.execute(QUERY,(bye_player[0], ))
            db.commit()
            
            #removing the bye player from the list
            ps.pop(ps.index(bye_player))
            swiss_pairs = []

            #pairing up players with similar standings
            for i in range(0,len(ps),2):
                #recording into matches with swiss pairs
                match = (ps[i][0],ps[i][1],ps[i+1][0],ps[i+1][1]) 

                #inserting swiss pair into matches table
                QUERY = "insert into matches (firstplayerid,secondplayerid) values (%s,%s)"
                c.execute(QUERY,(match[0],match[2]))
                db.commit()

                swiss_pairs.append(match) #adding the pairs to the list
            db.close()
            return swiss_pairs
