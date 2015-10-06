#!/usr/bin/env python
import sys, os
import oauth2 as oauth
import xml.etree.ElementTree as ET
import re
import calendar
import datetime
import math

sys.path.append('/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'OneStopFantasy.settings'
import django
django.setup()
from YqlConnect.models import Athlete, SeasonAverages, DailyData, LastTenGameAverages, LastFiveGameAverages
from django.db.models import Count, Min, Sum, Avg

print("Connection to Yql started!")

consumer = oauth.Consumer(key="dj0yJmk9NW9hRjlSeURqS0toJmQ9WVdrOWNqRlJUM1ZRTjJzbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lYg--", 
    secret="8a79e55ffaa18b24f74ddae0faddb4ba31c31d59")

statList = ['points', 'rebounds','assists','steals','blocks','threePointsMade','turnovers','fieldGoalPercentage','freeThrowPercentage']

def getLast(numberGames):

	AllAthletes = Athlete.objects.all();
	for athlete in AllAthletes:
		stdList = []
		meanList = []
		# check if there are 10 games recorded in dailydata, remember games are only considered if the player records a stat
		if DailyData.objects.filter(athlete = athlete).count() >= numberGames:
			lastSets = DailyData.objects.filter(athlete = athlete).order_by('gameDate')[:10][::-1]
			# for data in lastSets:
			# 	print str(data.gameDate) + ' ' + str(data.__dict__['points'])+ ' ' + str(athlete.__dict__['firstName'])
			for i in range (0,9):
				meanSum = 0
				for data in lastSets:
					meanSum = meanSum+data.__dict__[statList[i]]
				mean = meanSum/numberGames
				meanList.append(mean)
				# calculate std dev from mean
				stdDevSum = 0;
				for data in lastSets:
					stdDevSum = math.pow((data.__dict__[statList[i]] - meanList[i]),2)

				stdDev = math.sqrt(stdDevSum/numberGames)
				stdList.append(stdDev)
			lastGameAverages = ''
			if (numberGames == 10):
				LastGameAverages = LastTenGameAverages
			elif (numberGames == 5):
				LastGameAverages = LastFiveGameAverages
			if LastGameAverages.objects.filter(athlete = athlete).exists():
				lastGameAverages = LastGameAverages.objects.get(athlete = athlete)
				lastGameAverages.delete()
			lastGameAverages = LastGameAverages(
										athlete = athlete,
										points = meanList[0],
									    rebounds = meanList[1],
									    assists = meanList[2],
									    steals = meanList[3],
									    blocks = meanList[4],
									    threePointsMade = meanList[5],
									    turnovers = meanList[6],
									    fieldGoalPercentage = meanList[7],
									    freeThrowPercentage = meanList[8],
									    points_Std = stdList[0],
									    rebounds_Std = stdList[1],
									    assists_Std = stdList[2],
									    steals_Std = stdList[3],
									    blocks_Std = stdList[4],
									    threePointsMade_Std = stdList[5],
									    turnovers_Std = stdList[6],
									    fieldGoalPercentage_Std = stdList[7],
									    freeThrowPercentage_Std = stdList[8]
										)
			lastGameAverages.save()


	# if DailyData.objects.filter(athlete=athlete,gameDate = year+'-'+month+'-'+day).exists():
	# 	dailyData = DailyData.objects.get(athlete=athlete,gameDate = year+'-'+month+'-'+day)
	# 	dailyData.delete() 
	# # if noGamesPlayed == False:
	# dailyData = DailyData(athlete = athlete, points = points, rebounds = rebounds, assists = assists, steals = steals, blocks = blocks, threePointsMade = threePointsMade, turnovers = turnovers, fieldGoalPercentage = fieldGoalPercentage, freeThrowPercentage = freeThrowPercentage, gameDate = year+'-'+month+'-'+day )
	# dailyData.save()

def run():
	getLast(5)

run()




