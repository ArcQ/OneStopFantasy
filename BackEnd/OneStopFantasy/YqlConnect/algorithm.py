import numpy as np
import sys, os
import heapq as hp
# if __name__ == '__main__':    

sys.path.append('/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'OneStopFantasy.settings'
import django
django.setup()
# your imports, e.g. Django models
from YqlConnect.models import SeasonAverages, Athlete, FantasyTeam, FantasyTeamToAthlete, LeagueToFreeAgent,LeagueToUser

class Algorithm:

	def __init__(self,fantasyTeamId):
		self.fantasyTeam_Id = fantasyTeamId
		self.league_Id = fantasyTeamId.split(".")
		self.league_Id = self.league_Id[0]+'.'+self.league_Id[1]+'.'+self.league_Id[2]
	
	def averageScores(self):
		averageScores=[]
		athleteScores=[]
		pointsSum = 0
		reboundsSum = 0
		assistsSum = 0
		blocksSum = 0
		threePointsSum = 0
		turnoversSum = 0
		stealsSum = 0
		fieldGoalpercentage = 0
		freeThrowpercentage = 0
		counter = 0
		
		#seasonAverages = SeasonAverages.objects.all()
		for seasonAverages in SeasonAverages.objects.all():
			counter += 1
			pointsSum += seasonAverages.points
			reboundsSum += seasonAverages.rebounds
			assistsSum += seasonAverages.assists
			stealsSum += seasonAverages.steals
			blocksSum += seasonAverages.blocks
			threePointsSum += seasonAverages.threePointsMade
			turnoversSum += seasonAverages.turnovers 
			fieldGoalpercentage += seasonAverages.fieldGoalPercentage
			freeThrowpercentage += seasonAverages.freeThrowPercentage
		
		athleteScores.append(pointsSum)
		athleteScores.append(reboundsSum)
		athleteScores.append(assistsSum)
		athleteScores.append(stealsSum)
		athleteScores.append(blocksSum)
		athleteScores.append(threePointsSum)
		athleteScores.append(turnoversSum)
		athleteScores.append(fieldGoalpercentage)
		athleteScores.append(freeThrowpercentage)
		averageScores = [x / counter for x in athleteScores]
		return averageScores
		
	def calculateScore(self,athleteContainerList):
		athleteScores=[]
		pointsSum = 0
		reboundsSum = 0
		assistsSum = 0
		blocksSum = 0
		threePointsSum = 0
		turnoversSum = 0
		stealsSum = 0
		fieldGoalpercentage = 0
		freeThrowpercentage = 0
		for athleteContainer in athleteContainerList:
			seasonAverages = SeasonAverages.objects.get(athlete = athleteContainer.athlete)
			#sum all the categories in the athlete container
			pointsSum += seasonAverages.points
			reboundsSum += seasonAverages.rebounds
			assistsSum += seasonAverages.assists
			stealsSum += seasonAverages.steals
			blocksSum += seasonAverages.blocks
			threePointsSum += seasonAverages.threePointsMade
			turnoversSum += seasonAverages.turnovers 
			fieldGoalpercentage += seasonAverages.fieldGoalPercentage
			freeThrowpercentage += seasonAverages.freeThrowPercentage
		fieldGoalpercentage = fieldGoalpercentage/13
		freeThrowpercentage = freeThrowpercentage/13
		#before appending the percentages divide by 13
		
		athleteScores.append(pointsSum)
		athleteScores.append(reboundsSum)
		athleteScores.append(assistsSum)
		athleteScores.append(stealsSum)
		athleteScores.append(blocksSum)
		athleteScores.append(threePointsSum)
		athleteScores.append(turnoversSum)
		athleteScores.append(fieldGoalpercentage)
		athleteScores.append(freeThrowpercentage)
		#print athleteScores
		return athleteScores
		
	def calculateAddDropDecision(self,athleteContainerList,statCategoriesList, averageScores):
		freeAgentList= []
		for athleteContainer in athleteContainerList:
			playerSum = 0
			seasonAverages = SeasonAverages.objects.get(athlete = athleteContainer.athlete)
			for x in xrange(0,4): #4 dynamic number
				if statCategoriesList[x] == 0:
					playerSum += (seasonAverages.points / averageScores[0])
				elif statCategoriesList[x] == 1:
					playerSum += (seasonAverages.rebounds / averageScores[1]) 
				elif statCategoriesList[x] == 2:
					playerSum += (seasonAverages.assists / averageScores[2])
				elif statCategoriesList[x] == 3:
					playerSum += (seasonAverages.steals / averageScores[3])
				elif statCategoriesList[x] == 4:
					playerSum += (seasonAverages.blocks / averageScores[4])
				elif statCategoriesList[x] == 5:
					playerSum += (seasonAverages.threePointsMade / averageScores[5])
				elif statCategoriesList[x] == 6:
					playerSum -= (seasonAverages.turnovers / averageScores[6])
				elif statCategoriesList[x] == 7:
					playerSum += (seasonAverages.fieldGoalPercentage / averageScores[7])
				elif statCategoriesList[x] == 8:
					playerSum += (seasonAverages.freeThrowPercentage / averageScores[8])
			freeAgentList.append(playerSum)
		return freeAgentList
		
	def getDecision(self):
		
		#current team averages
		ownedScores = []
		ownedFantasyTeamToAthletes = FantasyTeamToAthlete.objects.filter(fantasyTeam = self.fantasyTeam_Id)
		ownedScores = self.calculateScore(ownedFantasyTeamToAthletes)
		#opponent team averages
		opponentScores = []
		oppFantasyTeamToAthletes = FantasyTeamToAthlete.objects.filter(fantasyTeam = '342.l.46555.t.7')
		opponentScores = self.calculateScore(oppFantasyTeamToAthletes)
		
		#calculating the difference between the averages
		comparison = []
		for x in xrange(0,8):
			if x == 6:
				difference = opponentScores[x]-ownedScores[x]
				comparison.append(difference)
			else:	
				difference = ownedScores[x]-opponentScores[x]
				comparison.append(difference)
		#taking the n categories you want to maximize
		max_values = hp.nlargest(5, xrange(len(comparison)), comparison.__getitem__)
		
		avgScores = self.averageScores()
		
		freeAgentScores = []
		freeAgents = LeagueToFreeAgent.objects.filter(league_Id=self.league_Id)
		freeAgentScores = self.calculateAddDropDecision(freeAgents, max_values, avgScores)
		
		dropDecisionPlayers = [] 
		dropDecisions = FantasyTeamToAthlete.objects.filter(fantasyTeam = self.fantasyTeam_Id)
		dropDecisionPlayers = self.calculateAddDropDecision(dropDecisions, max_values, avgScores)
		
		MaximumPlayer = 1
		MaximumPlayer += int(np.argmax(freeAgentScores))
		
		MinimumPlayer = 1
		MinimumPlayer += int(np.argmin(dropDecisionPlayers))
		
		
		print 'Based on you and your opponents Season averages'
		counter = 0
		for a in max_values:
			
			if comparison[a] >= 0:
				counter += 1
				if a == 0:
					print 'You will beat your opponent in points on average by '
					print comparison[a]
				elif a == 1:
					print 'You will beat your opponent in rebounds on average by '
					print comparison[a]
				elif a == 2:
					print 'You will beat your opponent in assists on average by '
					print comparison[a]
				elif a == 3:
					print 'You will beat your opponent in steals on average by '
					print comparison[a]
				elif a == 4:
					print 'You will beat your opponent in blocks on average by '
					print comparison[a]
				elif a == 5:
					print 'You will beat your opponent in three points made on average by '
					print comparison[a]
				elif a == 6:
					print 'You will beat your opponent in turnovers on average by '
					print comparison[a]
				elif a == 7:
					print 'You will beat your opponent in Field Goal Percentage on average by '
					print comparison[a]
				elif a == 8:
					print 'You will beat your opponent in Free Throw Percentage on average by '
					print comparison[a]

		if counter < 5:
			print 'You are unlikely to win this week as a result of your team'	
		
		dropIds = []
		addIds = []
		DropId = dropDecisions[MinimumPlayer].athlete.id
		dropIds.append(DropId)
		
		addPoints = []
		for x in xrange(0,10):
			MaxValue = MaximumPlayer + x
			AddId =  freeAgents[MaxValue].athlete.id	
			addIds.append(AddId)
		
		AddDropPairs = []
		for x in xrange (0,1):
			for y in xrange (0,10):
				AddDropPairs.append(str(dropIds[x])+","+str(addIds[y]))
				
		print AddDropPairs
		#print dropIds
		#print addIds
		#print dropIds[1]

		return {'drops':dropIds,'adds':addIds,'comparison':comparison}
		
		#print "Drop This Player"
		#print dropDecisions[MinimumPlayer].athlete.firstName
		#print dropDecisions[MinimumPlayer].athlete.lastName
		
		#print "Add This Player"   
		#print freeAgents[MaximumPlayer].athlete.firstName
		#print freeAgents[MaximumPlayer].athlete.lastName
			
# print 'started'
algorithm = Algorithm('342.l.46555.t.9')
algorithm.getDecision();
			
		MinimumPlayer = 1
		MinimumPlayer += int(np.argmin(ownedScores))


		print "Drop This Player"
		print ownedFantasyTeamToAthletes[MinimumPlayer].athlete.firstName
		print min(ownedScores)	

		print " "
		print "Add This Player"
		print freeAgents[MaximumPlayer].athlete.firstName

		print max(freeAgentScores)

		self.result = [ownedFantasyTeamToAthletes[MinimumPlayer].athlete,freeAgents[MaximumPlayer].athlete]
		return self.result

raw_input()