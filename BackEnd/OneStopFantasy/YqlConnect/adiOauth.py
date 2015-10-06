import sys, os
from oauth_hook import OAuthHook
import requests
import xml.etree.ElementTree as ET
import re

sys.path.append('/home/ubuntu/Fydp/onestopfantasyassistant/BackEnd/OneStopFantasy/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'OneStopFantasy.settings'
import django
django.setup()
# your imports, e.g. Django models
from YqlConnect.models import LeagueToUser, LeagueToFreeAgent, UserExtended

from django.contrib.auth.models import User
from YqlConnect.models import FantasyTeam
from YqlConnect.models import FantasyTeamToAthlete
from YqlConnect.models import Athlete

print("Connection to Yql started!")

base_url = 'http://fantasysports.yahooapis.com/fantasy/v2/'
url_FindLeagues = base_url+'users;use_login=1/games;game_keys=342/leagues'

#hack
username = 'eddiedev'
#for opponent teams that don't have a user attached
default_username = 'osfa'
user = ''
if User.objects.filter(username=username).exists():
        user = User.objects.get(username = username)
        userExtended = UserExtended.objects.get(user = user)
        access_Token = userExtended.access_Token
        access_Token_Secret = userExtended.access_Token_Secret

oauth_hook = OAuthHook(access_token=access_Token , access_token_secret=access_Token_Secret, consumer_key="dj0yJmk9NW9hRjlSeURqS0toJmQ9WVdrOWNqRlJUM1ZRTjJzbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lYg--", consumer_secret="8a79e55ffaa18b24f74ddae0faddb4ba31c31d59", header_auth=True)
request = requests.Request('GET', url_FindLeagues)
request = oauth_hook(request)
session = requests.session()

request = requests.Request('GET', url_FindLeagues)
request = oauth_hook(request)
response = session.send(request.prepare())
content = response.content
rosterXmlString = re.sub(' xmlns="[^"]+"', '', content, count=1)
root = ET.fromstring(rosterXmlString)
print content
