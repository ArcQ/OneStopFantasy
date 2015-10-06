# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YqlConnect', '0003_auto_20150309_0555'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyData',
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
                ('gameDate', models.DateField()),
                ('athlete', models.OneToOneField(related_name='Athlete_DailyData', null=True, to='YqlConnect.Athlete')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LastTenGameAverages',
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
                ('points_Std', models.FloatField(default=0.0)),
                ('rebounds_Std', models.FloatField(default=0.0)),
                ('assists_Std', models.FloatField(default=0.0)),
                ('steals_Std', models.FloatField(default=0.0)),
                ('blocks_Std', models.FloatField(default=0.0)),
                ('threePointsMade_Std', models.FloatField(default=0.0)),
                ('turnovers_Std', models.FloatField(default=0.0)),
                ('fieldGoalPercentage_Std', models.FloatField(default=0.0)),
                ('freeThrowPercentage_Std', models.FloatField(default=0.0)),
                ('athlete', models.OneToOneField(related_name='Athlete_LastTenGameAverages', null=True, to='YqlConnect.Athlete')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LastTwentyGameAverages',
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
                ('points_Std', models.FloatField(default=0.0)),
                ('rebounds_Std', models.FloatField(default=0.0)),
                ('assists_Std', models.FloatField(default=0.0)),
                ('steals_Std', models.FloatField(default=0.0)),
                ('blocks_Std', models.FloatField(default=0.0)),
                ('threePointsMade_Std', models.FloatField(default=0.0)),
                ('turnovers_Std', models.FloatField(default=0.0)),
                ('fieldGoalPercentage_Std', models.FloatField(default=0.0)),
                ('freeThrowPercentage_Std', models.FloatField(default=0.0)),
                ('athlete', models.OneToOneField(related_name='Athlete_LastTwentyGameAverages', null=True, to='YqlConnect.Athlete')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='weeklydata',
            name='athlete',
        ),
        migrations.DeleteModel(
            name='WeeklyData',
        ),
        migrations.AddField(
            model_name='athlete',
            name='injury',
            field=models.BooleanField(default=False, max_length=200),
            preserve_default=False,
        ),
    ]
