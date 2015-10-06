from django.contrib.auth.models import User, Group
from YqlConnect.models import SeasonAverages, Athlete, FantasyTeamToAthlete, FantasyTeam
from rest_framework import serializers

class SeasonAveragesSerializer(serializers.ModelSerializer):
    # athlete = AthleteSerializer()
    class Meta:
        model = SeasonAverages
        fields = ('points','rebounds','assists','steals','blocks','threePointsMade', 'turnovers', 'fieldGoalPercentage', 'freeThrowPercentage')

class AthleteSerializer(serializers.ModelSerializer):
    seasonaverages_set = SeasonAveragesSerializer(many=True, read_only=True)
    class Meta:
        model = Athlete
        fields = ('id','firstName', 'lastName','seasonaverages_set')

class FantasyTeamToAthleteSerializer(serializers.ModelSerializer):
    athlete = AthleteSerializer()
    class Meta:
        model = FantasyTeamToAthlete
        fields = ('athlete', 'fantasyTeam')

class UserFantasyTeamSerializer(serializers.ModelSerializer):
    fantasyteamtoathlete_set = FantasyTeamToAthleteSerializer()
    class Meta:
        model = FantasyTeam
        fields = ('user', 'teamName','fantasyteamtoathlete_set')
