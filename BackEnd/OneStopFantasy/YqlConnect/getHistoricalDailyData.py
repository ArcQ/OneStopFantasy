#!/usr/bin/env python
import sys, os
import oauth2 as oauth
import xml.etree.ElementTree as ET
import re
import calendar
import datetime

sys.path.append('/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'OneStopFantasy.settings'
import django
django.setup()
from YqlConnect.models import Athlete,SeasonAverages, DailyData

print("Connection to Yql started!")

consumer = oauth.Consumer(key="dj0yJmk9NW9hRjlSeURqS0toJmQ9WVdrOWNqRlJUM1ZRTjJzbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lYg--", 
    secret="8a79e55ffaa18b24f74ddae0faddb4ba31c31d59")

def getDailyStats(year,month,day):
	
	for i in range(0,24):

		start = i*24
		count = start+24
		# seasonAveragesUrl = 'http://fantasysports.yahooapis.com/fantasy/v2/game/342/players;start='+str(start)+';count='+str(count)+';status=ALL;sort=AR/stats'
		
		print year+'-'+month+'-'+day
		dailyStatsUrl = 'http://fantasysports.yahooapis.com/fantasy/v2/game/nba/players;start='+str(start)+';count='+str(count)+';status=ALL;sort=AR/stats;type=date;date='+year+'-'+month+'-'+day+'/'


		# Create our client
		client = oauth.Client(consumer)

		# The OAuth Client request works just like httplib2 for the most part.
		resp, content = client.request(dailyStatsUrl, "GET")
		# print resp
		# print content
		xmlstring = re.sub(' xmlns="[^"]+"', '', content, count=1)
		root = ET.fromstring(xmlstring)
		players = root[0].find('players')
		for player in players.findall('player'):
			for child in player:
				if child.tag == 'player_id':
					playerid = child.text
				elif child.tag == 'name':
					firstName = child.find('first').text
					lastName = child.find('last').text
					print  firstName + ' ' + lastName
				elif child.tag == 'player_stats':
					stats = child.find('stats')
					for stat in stats.findall('stat'):
						# noGamesPlayed = False
						#incase the player has never played a game which would give an undefined value
						try:
							if  stat.find('stat_id').text == '5':
								fieldGoalPercentage = float(stat.find('value').text)
							elif  stat.find('stat_id').text == '8':
								freeThrowPercentage = float(stat.find('value').text)
							elif  stat.find('stat_id').text == '10':
								threePointsMade = float(stat.find('value').text)
							elif  stat.find('stat_id').text == '12':
								points = float(stat.find('value').text)
							elif  stat.find('stat_id').text == '15':
								rebounds = float(stat.find('value').text)
							elif  stat.find('stat_id').text == '16':
								assists = float(stat.find('value').text)
							elif  stat.find('stat_id').text == '17':
								steals = float(stat.find('value').text)
							elif  stat.find('stat_id').text == '18':
								blocks = float(stat.find('value').text)
							elif  stat.find('stat_id').text == '19':
								turnovers = float(stat.find('value').text)
						except:
								# noGamesPlayed = True
								fieldGoalPercentage = 0
								freeThrowPercentage = 0
								threePointsMade = 0
								points = 0
								rebounds = 0
								assists = 0
								steals = 0
								blocks = 0
								turnovers = 0
								pass
					if (fieldGoalPercentage>0) or (freeThrowPercentage>0) or (threePointsMade>0) or (points>0) or (rebounds>0) or (assists>0) or (steals>0) or (blocks>0) or (turnovers>0):
						# Save Data into Database
						athlete = ''
						if Athlete.objects.filter(id=playerid).exists():
							athlete = Athlete.objects.get(id = playerid)

						if DailyData.objects.filter(athlete=athlete,gameDate = year+'-'+month+'-'+day).exists():
							dailyData = DailyData.objects.get(athlete=athlete,gameDate = year+'-'+month+'-'+day)
							dailyData.delete() 
						# if noGamesPlayed == False:
						dailyData = DailyData(athlete = athlete, points = points, rebounds = rebounds, assists = assists, steals = steals, blocks = blocks, threePointsMade = threePointsMade, turnovers = turnovers, fieldGoalPercentage = fieldGoalPercentage, freeThrowPercentage = freeThrowPercentage, gameDate = year+'-'+month+'-'+day )
						dailyData.save()

def run():
	year = 2014
	# for month in range(9,12):
	# 	# monthrange(year, month) Returns weekday of first day of the month and number of days in month, for the specified year and month.
	# 	for day in range(1,calendar.monthrange(year, month)[1]):
	# 		# set format to be 01,02 for months and days less than 10
	# 		month = '0'+str(month) if month<10 else str(month)
	# 		day = '0'+str(month) if day<10 else str(day)
	# 		getDailyStats(str(year),month,day)
	year = 2015
	# monthrange(year, month) Returns weekday of first day of the month and number of days in month, for the specified year and month.
	
	# month = 3
	# for day in range(1,9):
	# 	# set format to be 01,02 for months and days less than 10
	# 	month = '0'+str(month) if month<10 else str(month)
	# 	day = '0'+str(day) if day<10 else str(day)
	# 	getDailyStats(str(year),month,day)

	# for month in range(2,3):
	month = 2
	 	# monthrange(year, month) Returns weekday of first day of the month and number of days in month, for the specified year and month.
 	for day in range(1,calendar.monthrange(year, month)[1]):
 		# set format to be 01,02 for months and days less than 10
 		month = '0'+str(month) if month<10 else str(month)
 		day = '0'+str(day) if day<10 else str(day)
 		getDailyStats(str(year),month,day)

text_file = open("/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/YqlConnect/getHistoricalData.log", "a")
text_file.write("Script Run: %s \n" % datetime.datetime.now())
text_file.close()
run()
# run()




