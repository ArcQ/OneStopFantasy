import sys, os
from oauth_hook import OAuthHook
import requests
import xml.etree.ElementTree as ET
import re


sys.path.append('/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'OneStopFantasy.settings'
import django
django.setup()
from django.contrib.auth.models import User

# your imports, e.g. Django models
from YqlConnect.models import LeagueToUser
from YqlConnect.models import FantasyTeam,FantasyTeamToAthlete,Athlete,UserExtended,LeagueToFreeAgent


print("Connection to Yql started!")



class ConnectToYqlOauth():
	base_url = 'http://fantasysports.yahooapis.com/fantasy/v2/'
	def __init__(self,username):
		self.username = username
		#for opponent teams that don't have a user attached
		self.default_username = 'osfa_default'
		# this.defaultUser = ''
		# this.user = ''
		# access_Token = ''
		# access_Token_Secret = ''
		if User.objects.filter(username=username).exists():
		        self.user = User.objects.get(username = username)
		        userExtended = UserExtended.objects.get(user = self.user)
		        self.access_Token = userExtended.access_Token
		        self.access_Token_Secret = userExtended.access_Token_Secret
		if User.objects.filter(username=self.default_username).exists():
		        self.defaultUser = User.objects.get(username = username)

		self.oauth_hook = OAuthHook(access_token=self.access_Token , access_token_secret=self.access_Token_Secret, consumer_key="dj0yJmk9NW9hRjlSeURqS0toJmQ9WVdrOWNqRlJUM1ZRTjJzbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lYg--", consumer_secret="8a79e55ffaa18b24f74ddae0faddb4ba31c31d59", header_auth=True)
		self.session = requests.session()

	def FindAllTeams(self,session,league_Id):
		url_FindOtherTeamsInLeague = ConnectToYqlOauth.base_url+'league/'+league_Id.text+'/teams'
		request = requests.Request('GET', url_FindOtherTeamsInLeague)
		request = self.oauth_hook(request)
		response = self.session.send(request.prepare())
		content = response.content
		rosterXmlString = re.sub(' xmlns="[^"]+"', '', content, count=1)
		teams = ET.fromstring(rosterXmlString).find('league').find('teams')
		print content
		for team in teams.findall('team'):
			team_Key = team.find('team_key')
			team_Name = team.find('name')

			#Save Data into Database
			opponentUser = ''
			if FantasyTeam.objects.filter(id=team_Key.text).exists():
				fantasyTeam = FantasyTeam.objects.get(id=team_Key.text)
				opponentUser = User.objects.get(username = fantasyTeam.user.username)
				FantasyTeamToAthlete.objects.filter(fantasyTeam = fantasyTeam).delete()
			else:
				opponentUser = defaultUser
			fantasyTeam = FantasyTeam(id=team_Key.text, teamName=team_Name.text, user=opponentUser, league_Id= league_Id.text)
			fantasyTeam.save()

			self.FindRosters(team_Key.text)

	def FindOwnTeam(self,session,user,league_Id):
		url_FindTeams = ConnectToYqlOauth.base_url+'users;use_login=1/games;game_keys=342/teams'
		request = requests.Request('GET', url_FindTeams)
		request = self.oauth_hook(request)
		response = self.session.send(request.prepare())
		content = response.content
		rosterXmlString = re.sub(' xmlns="[^"]+"', '', content, count=1)
		root = ET.fromstring(rosterXmlString)
		games = root.find('users').find('user').find('games')
		for game in games.findall('game'):
			if game.find('game_key').text == '342':
				teams = game.find('teams')
				for team in teams.findall('team'):
					team_Key = team.find('team_key')
					team_Name = team.find('name')
					#Save Data into Database
					if FantasyTeam.objects.filter(id=team_Key.text).exists():
						fantasyTeam = FantasyTeam.objects.get(id=team_Key.text)
						FantasyTeamToAthlete.objects.filter(fantasyTeam = fantasyTeam).delete()
					fantasyTeam = FantasyTeam(id=team_Key.text, teamName=team_Name.text, user=user, league_Id= league_Id.text)
					fantasyTeam.save()
					self.FindRosters(team_Key.text)

	def FindRosters(self,team_Key_Text):
		url_FindRosters = ConnectToYqlOauth.base_url+'team/'+team_Key_Text+'/roster/players'
		request = requests.Request('GET', url_FindRosters)
		request = self.oauth_hook(request)
		response = self.session.send(request.prepare())
		content = response.content
		rosterXmlString = re.sub(' xmlns="[^"]+"', '', content, count=1)
		root = ET.fromstring(rosterXmlString)
		players = root.find('team').find('roster').find('players')
		for player in players.findall('player'):
			player_Key = player.find('player_id')
			#Save Data into Database
			fantasyTeam = FantasyTeam.objects.get(id = team_Key_Text)
			try:
				fantasyTeamToAthlete = FantasyTeamToAthlete(fantasyTeam=fantasyTeam, athlete=Athlete.objects.get(id = player_Key.text))
				fantasyTeamToAthlete.save()
			except Exception as e:
				print e

	def FindAllFreeAgentsToLeague(self,team_Key_Text,league_Id):

		if LeagueToFreeAgent.objects.filter(league_Id=league_Id.text).exists():
			leagueToFreeAgent = LeagueToFreeAgent.objects.filter(league_Id=league_Id.text)
			leagueToFreeAgent.delete() 

		for i in range(0,5):
			start = i*24
			count = start+24
			url_FindOtherTeamsInLeague = ConnectToYqlOauth.base_url+'league/'+league_Id.text+'/players;start='+str(start)+';count='+str(count)+';status=FA;sort=AR/'

			request = requests.Request('GET', url_FindOtherTeamsInLeague)
			request = self.oauth_hook(request)
			response = self.session.send(request.prepare())
			content = response.content
			print content
			xmlstring = re.sub(' xmlns="[^"]+"', '', content, count=1)
			root = ET.fromstring(xmlstring)
			players = root[0].find('players')

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

			for player in players.findall('player'):
				for child in player:
					if child.tag == 'player_id':
						playerid = child.text
					elif child.tag == 'name':
						firstName = child.find('first').text
						lastName = child.find('last').text

						# Save Data into Database
						try:
							athlete = Athlete.objects.get(id = playerid)
							# if noGamesPlayed == False:
							leagueToFreeAgent = LeagueToFreeAgent(athlete = athlete, league_Id=league_Id.text)
							leagueToFreeAgent.save()
						except Exception as e:
							print e

	def getAllUserInformation(self):
		try:
			url_FindLeagues = ConnectToYqlOauth.base_url+'users;use_login=1/games;game_keys=342/leagues'
			request = requests.Request('GET', url_FindLeagues)
			request = self.oauth_hook(request)
			response = self.session.send(request.prepare())
			content = response.content
			xmlstring = re.sub(' xmlns="[^"]+"', '', content, count=1)
			root = ET.fromstring(xmlstring)
			games = root.find('users').find('user').find('games')
			league_key = ''
			for game in games.findall('game'):
				if game.find('game_key').text == '342':
					leagues = game.find('leagues')
					for league in leagues.findall('league'):
						league_key = league.find('league_key')
						self.FindOwnTeam(self.session,self.user,league_key)
						self.FindAllTeams(self.session,league_key)
						self.FindAllFreeAgentsToLeague(self.session,league_key)
			return 'Successful Yahoo User Information Retrieval'
		except Exception as e:
			return 'error: '+e





