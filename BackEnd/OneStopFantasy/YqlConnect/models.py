from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Athlete(models.Model):
    id = models.IntegerField(primary_key = True)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    profileUrl = models.CharField(max_length=200)
    team = models.CharField(max_length=200)
    injury = models.BooleanField(max_length=200)
    positions = models.CharField(max_length=200)
    def __str__(self):
        return self.firstName+' '+self.lastName

class DailyData(models.Model):
    athlete = models.ForeignKey(Athlete, null = True, related_name = 'Athlete_DailyData')
    points = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    steals = models.FloatField(default=0.0)
    blocks = models.FloatField(default=0.0)
    threePointsMade = models.FloatField(default=0.0)
    turnovers = models.FloatField(default=0.0)
    fieldGoalPercentage = models.FloatField(default=0.0)
    freeThrowPercentage = models.FloatField(default=0.0)
    gameDate = models.DateField()
    def __str__(self):
        return self.athlete.firstName+self.athlete.lastName+' : '+str(self.gameDate)

class LastTenGameAverages(models.Model):
    athlete = models.OneToOneField(Athlete, null = True, related_name = 'Athlete_LastTenGameAverages')
    points = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    steals = models.FloatField(default=0.0)
    blocks = models.FloatField(default=0.0)
    threePointsMade = models.FloatField(default=0.0)
    turnovers = models.FloatField(default=0.0)
    fieldGoalPercentage = models.FloatField(default=0.0)
    freeThrowPercentage = models.FloatField(default=0.0)
    points_Std = models.FloatField(default=0.0)
    rebounds_Std = models.FloatField(default=0.0)
    assists_Std = models.FloatField(default=0.0)
    steals_Std = models.FloatField(default=0.0)
    blocks_Std = models.FloatField(default=0.0)
    threePointsMade_Std = models.FloatField(default=0.0)
    turnovers_Std = models.FloatField(default=0.0)
    fieldGoalPercentage_Std = models.FloatField(default=0.0)
    freeThrowPercentage_Std = models.FloatField(default=0.0)
    def __str__(self):
        return self.athlete.firstName+self.athlete.lastName

class LastFiveGameAverages(models.Model):
    athlete = models.OneToOneField(Athlete, null = True, related_name = 'Athlete_LastTwentyGameAverages')
    points = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    steals = models.FloatField(default=0.0)
    blocks = models.FloatField(default=0.0)
    threePointsMade = models.FloatField(default=0.0)
    turnovers = models.FloatField(default=0.0)
    fieldGoalPercentage = models.FloatField(default=0.0)
    freeThrowPercentage = models.FloatField(default=0.0)
    points_Std = models.FloatField(default=0.0)
    rebounds_Std = models.FloatField(default=0.0)
    assists_Std = models.FloatField(default=0.0)
    steals_Std = models.FloatField(default=0.0)
    blocks_Std = models.FloatField(default=0.0)
    threePointsMade_Std = models.FloatField(default=0.0)
    turnovers_Std = models.FloatField(default=0.0)
    fieldGoalPercentage_Std = models.FloatField(default=0.0)
    freeThrowPercentage_Std = models.FloatField(default=0.0)
    def __str__(self):
        return self.athlete.firstName+self.athlete.lastName

class MonthlyData(models.Model):
    athlete = models.ForeignKey(Athlete, null = True, related_name = 'Athlete_MonthlyData')
    points = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    steals = models.FloatField(default=0.0)
    blocks = models.FloatField(default=0.0)
    threePointsMade = models.FloatField(default=0.0)
    turnovers = models.FloatField(default=0.0)
    fieldGoalPercentage = models.FloatField(default=0.0)
    freeThrowPercentage = models.FloatField(default=0.0)
    points_Std = models.FloatField(default=0.0)
    rebounds_Std = models.FloatField(default=0.0)
    assists_Std = models.FloatField(default=0.0)
    steals_Std = models.FloatField(default=0.0)
    blocks_Std = models.FloatField(default=0.0)
    threePointsMade_Std = models.FloatField(default=0.0)
    turnovers_Std = models.FloatField(default=0.0)
    fieldGoalPercentage_Std = models.FloatField(default=0.0)
    freeThrowPercentage_Std = models.FloatField(default=0.0)
    month = models.DateField()
    def __str__(self):
        return self.athlete.firstName+self.athlete.lastName

class SeasonAverages(models.Model):
    athlete = models.OneToOneField(Athlete, null = True, related_name = 'Athlete_SeasonAverages')
    points = models.FloatField(default=0.0)
    rebounds = models.FloatField(default=0.0)
    assists = models.FloatField(default=0.0)
    steals = models.FloatField(default=0.0)
    blocks = models.FloatField(default=0.0)
    threePointsMade = models.FloatField(default=0.0)
    turnovers = models.FloatField(default=0.0)
    fieldGoalPercentage = models.FloatField(default=0.0)
    freeThrowPercentage = models.FloatField(default=0.0)
    def __str__(self):
        return self.athlete.firstName+self.athlete.lastName

class UserExtended(models.Model):
    user = models.OneToOneField(User, primary_key = True, related_name = 'UserExtended_User')
    access_Token = models.TextField (max_length=8000, null = True)
    access_Token_Secret = models.CharField(max_length=200, null = True)
    oauth_session_handle = models.CharField(max_length=200, null = True)
    oauth_Token = models.TextField (max_length=8000, null = True)
    oauth_Token_Secret = models.TextField (max_length=8000, null = True)
    oauth_Verifier = models.CharField(max_length=200, null = True)
    def __str__(self):
        return self.user.username

class LeagueToUser(models.Model):
    user = models.ForeignKey(User, related_name = 'LeagueToUser_User')
    league_Id = models.CharField(max_length=200)
    def __str__(self):
        return self.league_Id+' | '+self.user.username

class FantasyTeam(models.Model):
    id = models.CharField(max_length=200, primary_key = True) 
    teamName = models.CharField(max_length=200)
    user = models.ForeignKey(User, null = True, related_name = 'FantasyTeam_User')
    league_Id = models.CharField(max_length=200)
    def __str__(self):
        return self.teamName

# class Games(models.Model
class FantasyTeamToAthlete(models.Model):
    fantasyTeam = models.ForeignKey(FantasyTeam, null = True, related_name = 'FantasyTeamToAthlete_FantasyTeam')
    athlete = models.ForeignKey(Athlete, null = True, related_name = 'FantasyTeamToAthlete_Athlete')
    
class LeagueToFreeAgent(models.Model):
    athlete = models.ForeignKey(Athlete, null = True, related_name = 'LeagueToFreeAgents_Athlete')
    league_Id = models.CharField(max_length=200)

class PositionToAthlete(models.Model):
    position = models.CharField(null = True, max_length=5)
    athlete = models.ForeignKey(Athlete, null = True, related_name = 'PositionToAthlete_Athlete')

# class Positions(models.Model
