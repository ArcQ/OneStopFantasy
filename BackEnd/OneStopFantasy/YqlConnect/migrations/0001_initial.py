# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('firstName', models.CharField(max_length=200)),
                ('lastName', models.CharField(max_length=200)),
                ('profileUrl', models.CharField(max_length=200)),
                ('team', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FantasyTeam',
            fields=[
                ('id', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('teamName', models.CharField(max_length=200)),
                ('league_Id', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FantasyTeamToAthlete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('athlete', models.ForeignKey(related_name='FantasyTeamToAthlete_Athlete', to='YqlConnect.Athlete', null=True)),
                ('fantasyTeam', models.ForeignKey(related_name='FantasyTeamToAthlete_FantasyTeam', to='YqlConnect.FantasyTeam', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeagueToFreeAgent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('league_Id', models.CharField(max_length=200)),
                ('athlete', models.ForeignKey(related_name='LeagueToFreeAgents_Athlete', to='YqlConnect.Athlete', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LeagueToUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('league_Id', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeasonAverages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('points', models.FloatField(default=0.0)),
                ('rebounds', models.FloatField(default=0.0)),
                ('assists', models.FloatField(default=0.0)),
                ('steals', models.FloatField(default=0.0)),
                ('blocks', models.FloatField(default=0.0)),
                ('threePointsMade', models.FloatField(default=0.0)),
                ('turnovers', models.FloatField(default=0.0)),
                ('fieldGoalPercentage', models.FloatField(default=0.0)),
                ('freeThrowPercentage', models.FloatField(default=0.0)),
                ('athlete', models.OneToOneField(related_name='Athlete_SeasonAverages', null=True, to='YqlConnect.Athlete')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserExtended',
            fields=[
                ('user', models.OneToOneField(related_name='UserExtended_User', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('access_Token', models.TextField(max_length=8000)),
                ('access_Token_Secret', models.CharField(max_length=200)),
                ('oauth_session_handle', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='leaguetouser',
            name='user',
            field=models.ForeignKey(related_name='LeagueToUser_User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fantasyteam',
            name='user',
            field=models.ForeignKey(related_name='FantasyTeam_User', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
