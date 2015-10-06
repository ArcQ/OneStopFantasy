#!/usr/bin/env python
import sys, os
import oauth2 as oauth
import xml.etree.ElementTree as ET
import re
import calendar
import datetime
import time

sys.path.append('/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'OneStopFantasy.settings'
import django
django.setup()
from YqlConnect.models import Athlete, SeasonAverages, DailyData

print("Connection to Yql started!")

consumer = oauth.Consumer(key="dj0yJmk9NW9hRjlSeURqS0toJmQ9WVdrOWNqRlJUM1ZRTjJzbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lYg--", 
    secret="8a79e55ffaa18b24f74ddae0faddb4ba31c31d59")

# encodedUrl = "https://query.yahooapis.com/v1/public/yql?q="+urllib.quote("select * from fantasysports.games where game_key= ") +'nba&diagnostics=true'
# print encodedUrl;
# request_token_url = 'http://fantasysports.yahooapis.com/fantasy/v2/game/nba'
# request_token_url = 'http://fantasysports.yahooapis.com/fantasy/v2/player/342.p.4906/stats'

def getSeasonAverages():
	for i in range(0,25):
		start = i*24
		count = start+24
		seasonAveragesUrl = 'http://fantasysports.yahooapis.com/fantasy/v2/game/342/players;start='+str(start)+';count='+str(count)+';status=ALL;sort=AR/stats'


		# Create our client.
		client = oauth.Client(consumer)

		# The OAuth Client request works just like httplib2 for the most part.
		resp, content = client.request(seasonAveragesUrl, "GET")
		# print resp
		# print content

		xmlstring = re.sub(' xmlns="[^"]+"', '', content, count=1)
		root = ET.fromstring(xmlstring)
		players = root[0].find('players')
		for player in players.findall('player'):
			for child in player:
				status = child.find('status')
				if status is None:
					injury = False
				elif status.text == 'INJ':
					injury = True
				else:
					injury = False
				if child.tag == 'player_id':
					playerid = child.text
				elif child.tag == 'name':
					firstName = child.find('first').text
					lastName = child.find('last').text
				elif child.tag =='editorial_team_full_name':
					team = child.text
				elif child.tag =='display_position':
					positions = child.text
				elif child.tag == 'player_stats':
					stats = child.find('stats')
					for stat in stats.findall('stat'):
						# noGamesPlayed = False
						#incase the player has never played a game which would give an undefined value
						try:
							if stat.find('stat_id').text == '0':
								gamesPlayed = float(stat.find('value').text)
								# if noGamesPlayed == True:
							elif  stat.find('stat_id').text == '5':
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
								gamesPlayed = 1
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

					# Save Data into Database
					if Athlete.objects.filter(id=playerid).exists():
						athlete = Athlete.objects.get(id = playerid)
						athlete.delete()
					athlete = Athlete(id = playerid, firstName = firstName, lastName = lastName, injury = injury, team = team, positions = positions)
					athlete.save()

					if SeasonAverages.objects.filter(athlete=athlete).exists():
						seasonAverages = SeasonAverages.objects.get(id = playerid)
						seasonAverages.delete() 
					# if noGamesPlayed == False:
					seasonAverages = SeasonAverages(athlete = athlete, points = points/gamesPlayed, rebounds = rebounds/gamesPlayed, assists = assists/gamesPlayed, steals = steals/gamesPlayed, blocks = blocks/gamesPlayed, threePointsMade = threePointsMade/gamesPlayed, turnovers = turnovers/gamesPlayed, fieldGoalPercentage = fieldGoalPercentage, freeThrowPercentage = freeThrowPercentage )
					seasonAverages.save()

def getDailyStats(currentDate):
	
	for i in range(0,24):

		start = i*24
		count = start+24
		# seasonAveragesUrl = 'http://fantasysports.yahooapis.com/fantasy/v2/game/342/players;start='+str(start)+';count='+str(count)+';status=ALL;sort=AR/stats'
		
		print currentDate
		dailyStatsUrl = 'http://fantasysports.yahooapis.com/fantasy/v2/game/nba/players;start='+str(start)+';count='+str(count)+';status=ALL;sort=AR/stats;type=date;date='+currentDate+'/'


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

						if DailyData.objects.filter(athlete=athlete,gameDate = currentDate).exists():
							dailyData = DailyData.objects.get(athlete=athlete,gameDate = currentDate)
							dailyData.delete() 
						# if noGamesPlayed == False:
						dailyData = DailyData(athlete = athlete, points = points, rebounds = rebounds, assists = assists, steals = steals, blocks = blocks, threePointsMade = threePointsMade, turnovers = turnovers, fieldGoalPercentage = fieldGoalPercentage, freeThrowPercentage = freeThrowPercentage, gameDate = currentDate )
						dailyData.save()


def run():
	getSeasonAverages()
	## yyyy-mm-dd format
	currentDate = (time.strftime("%Y-%m-%d"))
	getDailyStats(currentDate)


run()
text_file = open("/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/YqlConnect/connectToYqlOutput.log", "a")
text_file.write("Script Run: %s \n" % datetime.datetime.now())
text_file.close()




