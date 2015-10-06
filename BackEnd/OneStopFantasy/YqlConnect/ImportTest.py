import numpy as np
import sys, os
# if __name__ == '__main__':    

sys.path.append('/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'OneStopFantasy.settings'
import django
django.setup()
# your imports, e.g. Django models
from YqlConnect.models import SeasonAverages, Athlete, FantasyTeam, FantasyTeamToAthlete, LeagueToFreeAgent,LeagueToUser

def calculateScore(athleteContainerList):
	athleteScores=[]
	for athleteContainer in athleteContainerList:
		seasonAverages = SeasonAverages.objects.get(athlete = athleteContainer.athlete)
		# freeAgentList.append(freeAgentSeasonAverages)
		playerSum = seasonAverages.points + seasonAverages.rebounds + seasonAverages.assists+ seasonAverages.steals + seasonAverages.blocks + seasonAverages.threePointsMade+ seasonAverages.turnovers+ seasonAverages.fieldGoalPercentage+ seasonAverages.freeThrowPercentage
		playerScore = playerSum * correlationCoefficient
		athleteScores.append(playerSum)
	return athleteScores

correlationCoefficient = 1

league = LeagueToUser.objects.filter(league_Id = "342.l.107573")

freeAgentScores= []
freeAgents = LeagueToFreeAgent.objects.filter(league=league)
freeAgentScores = calculateScore(freeAgents)
MaximumPlayer = 1
MaximumPlayer += int(np.argmax(freeAgentScores))

ownedScores = []
ownedFantasyTeamToAthletes = FantasyTeamToAthlete.objects.filter(fantasyTeam = "342.l.107573.t.1")
ownedScores = calculateScore(ownedFantasyTeamToAthletes)
MinimumPlayer = 1
MinimumPlayer += int(np.argmin(ownedScores))


print "Drop This Player"
print ownedFantasyTeamToAthletes[MinimumPlayer].athlete.firstName
print min(ownedScores)	

print " "
print "Add This Player"
print freeAgents[MaximumPlayer].athlete.firstName

print max(freeAgentScores)

# for fantasyTeamToAthlete in ownedFantasyTeamToAthletes:
# 	ownedSeasonAverages = SeasonAverages.objects.get(athlete = fantasyTeamToAthlete.athlete)
# 	# ownedList.append(ownedSeasonAverages)
# 	playerSum = ownedSeasonAverages.points + ownedSeasonAverages.rebounds + ownedSeasonAverages.assists+ ownedSeasonAverages.steals + ownedSeasonAverages.blocks + ownedSeasonAverages.threePointsMade+ freeAgentSeasonAverages.turnovers+ freeAgentSeasonAverages.fieldGoalPercentage+ freeAgentSeasonAverages.freeThrowPercentage






	# for i in range(0,14):
	# 	PlayerSum = 0
	# 	PlayerSum2 = 0
	# 	CorrelationCoefficient = 1

	# 	for j in range(0,8): #9 is the categories
	# 		PlayerSum = 
	# 		PlayerSum += float(matrix[x][y])
	# 		PlayerSum2 += float(matrix2[x][y])
	# 		PlayerScore = PlayerSum * CorrelationCoefficient
	# 		PlayerScore2 = PlayerSum2 * CorrelationCoefficient
	# 	PlayerscoreA.append(PlayerScore)
	# 	PlayerscoreA2.append(PlayerScore2)	

	# MinimumPlayer = 1
	# MaximumPlayer = 1
	
	# MinimumPlayer += int(np.argmin(PlayerscoreA))
	# MaximumPlayer += int(np.argmax(PlayerscoreA2))
	
	# print "Drop This Player"
	# print matrix[MinimumPlayer][0]
	# print min(PlayerscoreA)	
	
	# print " "
	# print "Add This Player"
	# print matrix2[MaximumPlayer][0]
	
	# print max(PlayerscoreA2)

# with open('Players.csv', 'rb') as file1, open('Players2.csv', 'rb') as file2:
# 	contents = csv.reader(file1)
# 	contents2 = csv.reader(file2)
	
# 	matrix = list()
# 	matrix2 = list()
	
# 	for row in contents:
# 		matrix.append(row)
	
# 	for row in contents2:
# 		matrix2.append(row)
	
# 	PlayerscoreA = []
# 	PlayerscoreA2 = []
	
# 	for x in xrange(1,15):
# 		PlayerSum = 0
# 		PlayerSum2 = 0
# 		CorrelationCoefficient = 1
# 		for y in xrange(1,9): #9 is the categories
# 			PlayerSum += float(matrix[x][y])
# 			PlayerSum2 += float(matrix2[x][y])
# 			PlayerScore = PlayerSum * CorrelationCoefficient
# 			PlayerScore2 = PlayerSum2 * CorrelationCoefficient
# 		PlayerscoreA.append(PlayerScore)
# 		PlayerscoreA2.append(PlayerScore2)
# 	#Need to keeep track of positions
	
# 	MinimumPlayer = 1
# 	MaximumPlayer = 1
	
# 	MinimumPlayer += int(np.argmin(PlayerscoreA))
# 	MaximumPlayer += int(np.argmax(PlayerscoreA2))
	
# 	print "Drop This Player"
# 	print matrix[MinimumPlayer][0]
# 	print min(PlayerscoreA)	
	
# 	print " "
# 	print "Add This Player"
# 	print matrix2[MaximumPlayer][0]
	
# 	print max(PlayerscoreA2)
	
# 	#uPER = (1 / MP) *
#      #[ 3P
#      #+ (2/3) * AST
#      #+ (2 - factor * (team_AST / team_FG)) * FG
#      #+ (FT *0.5 * (1 + (1 - (team_AST / team_FG)) + (2/3) * (team_AST / team_FG)))
#      #- VOP * TOV
#      #- VOP * DRB% * (FGA - FG)
#      #- VOP * 0.44 * (0.44 + (0.56 * DRB%)) * (FTA - FT)
#      #+ VOP * (1 - DRB%) * (TRB - ORB)
#      #+ VOP * DRB% * ORB
#      #+ VOP * STL
#      #+ VOP * DRB% * BLK
#      #- PF * ((lg_FT / lg_PF) - 0.44 * (lg_FTA / lg_PF) * VOP) ]
# raw_input()