from django.shortcuts import render
from django.http import HttpResponse
from models import SeasonAverages


def test(request):
	context={'name':'eddie','dbtable':SeasonAverages.objects.all()}
	return render(request, 'test.html', context)
# Create your views here.
