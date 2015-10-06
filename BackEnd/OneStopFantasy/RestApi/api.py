# myapp/api.py
from tastypie.resources import ModelResource
from YqlConnect.models import SeasonAverages, Athlete, FantasyTeam, FantasyTeamToAthlete, LeagueToFreeAgent,LeagueToUser
from tastypie import fields
from django.http import HttpResponse
from YqlConnect.algorithm import Algorithm
from tastypie.authentication import ApiKeyAuthentication,BasicAuthentication
from tastypie.authorization import Authorization  # , Authorization
from tastypie.exceptions import Unauthorized

from django.contrib.auth.models import User



class UserObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        # This assumes a ``QuerySet`` from ``ModelResource``.
        return object_list.filter(user=bundle.request.user)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def delete_list(self, object_list, bundle):
        # Sorry user, no deletes for you!
        raise Unauthorized("Sorry, no deletes.")

    def delete_detail(self, object_list, bundle):
        raise Unauthorized("Sorry, no deletes.")

class Login(ModelResource):
     class Meta:
        list_allowed_methods = ['get', 'post']
        queryset = User.objects.all()
        resource_name = 'login'
        # authentication = ApiKeyAuthentication()
        authorization = Authorization()

class SeasonAveragesResource(ModelResource):
    # athlete = AthleteSerializer()
    class Meta:
        queryset = SeasonAverages.objects.all()
        resource_name = 'SeasonAverages'
        max_limit = None

class AthleteResource(ModelResource):

    seasonaverages = fields.ToOneField(SeasonAveragesResource, 'Athlete_SeasonAverages', full=True)
    class Meta:
        queryset = Athlete.objects.all()
        resource_name = 'Athlete_SeasonAverages'
        max_limit = None


#FantasyTeam Resources, requires more complicated url linking and joins

class FantasyTeamToAthleteResource(ModelResource):
    athlete = fields.ForeignKey(AthleteResource, 'athlete', full=True)
    class Meta:
        model = FantasyTeamToAthlete
        queryset = FantasyTeamToAthlete.objects.all()
        resource_name = 'FantasyTeamToAthleteResource'
        max_limit = None


class FantasyTeamResource(ModelResource):
    fantasyTeamToAthlete = fields.ToManyField(FantasyTeamToAthleteResource, 'FantasyTeamToAthlete_FantasyTeam', full=True)
    class Meta:
        queryset = FantasyTeam.objects.all()
        resource = 'FantasyTeam'
        resource_name = 'FantasyTeam'
        max_limit = None
        authentication = ApiKeyAuthentication()
        authorization = UserObjectsOnlyAuthorization()

class CalculateDecisionResource(ModelResource):

    class Meta:
        resource_name = 'Decision'
        default_format = "application/json"

    def get_list(self, request, **kwargs):
        # Do any operation here and return in form of json in next line
        param =  request.GET['team_Id']
        algorithm = Algorithm(param)

        decisionPair =  algorithm.getDecision()
        return self.create_response(request,decisionPair)
class CheckUser(ModelResource):
    class Meta:
        model = User
	queryset = User.objects.all()
        filtering = {
            "username": ('exact',),
        }
	resource_name = 'User'

