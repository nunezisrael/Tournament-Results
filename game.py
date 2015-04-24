import tournament
import math
import bleach

print "Do you want clear previous tournament history? \n y = Yes \n n = No"
tdelete = str(bleach.clean(raw_input('==>')))
if tdelete == 'y':
    print "All tables wiped!"
    tournament.deleteMatches()
    tournament.deletePlayers()
elif tdelete == 'n':
    print "tournament unchanged!"
#Entering players into the tournament
print "Enter number of players"
players = int(bleach.clean(raw_input('==>')))

for i in range(players):
    print "Enter player's fullname"
    player = str(bleach.clean(raw_input()))
    tournament.registerPlayer(player)
    print "Player "+ player +" is registered for the tournament "

#Showing total number of players registered
total_players = tournament.countPlayers()
print ("A total of " +str(total_players)+" are registered for the game")

#Keeping track of rounds need to find a winner
try:
    total_rounds = int(math.ceil(math.log(total_players,2)))#rounding up matches
except ValueError,e:
    if total_players == 0:
        total_rounds = 0
        
rounds = 0

while rounds < total_rounds:
    rounds = rounds + 1
    print "Entering ROUND # "+ str(rounds)+" out of "+str(total_rounds)

    #Starting the tournament
    player_standings = tournament.playerStandings()
    print "Current Standings: \n"
    for standing in player_standings:
        print standing
        
    swiss_pairs = tournament.swissPairings()
    print "\n Swiss Pairs"
    if swiss_pairs == (None):
        print "No Pairs"
    else:
        for pair in swiss_pairs:
            print pair
            tournament.reportMatch(pair[0],pair[2])
            print "match winner: "+str(pair[0])

    if rounds == total_rounds:
        winner = tournament.playerStandings()[0][1]
        second_place = tournament.playerStandings()[1][1]
        loser = tournament.playerStandings()[total_players-1][1]
        print "TOURNAMENT WINNER is "+str(winner)
        #print "second place is "+str(second_place)+"\n  and loser is "+str(loser)








