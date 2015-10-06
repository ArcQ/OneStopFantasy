from django.contrib import admin
from YqlConnect.models import Athlete, SeasonAverages, FantasyTeam, UserExtended, FantasyTeamToAthlete, LeagueToUser, LeagueToFreeAgent, DailyData, LastTenGameAverages, LastFiveGameAverages, MonthlyData

class SeasonAveragesInLine(admin.StackedInline):
	model = SeasonAverages
	extra = 1

class AthleteAdmin(admin.ModelAdmin):
	inlines = [SeasonAveragesInLine]
	# list_display = ('firstName', 'lastName', 'team')

class SeasonAveragesAdmin(admin.ModelAdmin):
	list_display = ('name','points', 'rebounds','assists','steals','blocks','threePointsMade','turnovers','fieldGoalPercentage','freeThrowPercentage')
	def name(self, instance):
		return (instance.athlete.lastName+', '+instance.athlete.firstName)

class FantasyTeamToAthleteAdmin(admin.ModelAdmin):
	list_display = ('athlete','fantasyTeam')
	search_fields = ['athlete__firstName']

class FantasyTeamToAthleteInLine(admin.StackedInline):
	model = FantasyTeamToAthlete
	extra = 1

class FantasyTeamAdmin(admin.ModelAdmin):
	inlines = [FantasyTeamToAthleteInLine]

admin.site.register(Athlete,AthleteAdmin)
admin.site.register(SeasonAverages, SeasonAveragesAdmin)
admin.site.register(FantasyTeam,FantasyTeamAdmin)
admin.site.register(UserExtended)
admin.site.register(MonthlyData)
admin.site.register(LeagueToFreeAgent)
admin.site.register(DailyData)
admin.site.register(LastTenGameAverages)
admin.site.register(LastFiveGameAverages)
admin.site.register(FantasyTeamToAthlete, FantasyTeamToAthleteAdmin)

# #'name'
