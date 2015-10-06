from django.contrib.auth.models import User, Group
from YqlConnect.models import Athlete, FantasyTeamToAthlete, FantasyTeam
from rest_framework import viewsets
from RestApi.serializers import AthleteSerializer, UserFantasyTeamSerializer
import json
from django.http import HttpResponse



class AthleteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Athlete.objects.all()
    serializer_class = AthleteSerializer

class FantasyTeamViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

def test():
    response = {  
        'fantasyTeam': list(Athlete.objects.get(id=1).objects.firstName),
    }

    return HttpResponse(json.dumps(response), mimetype='application/json')



