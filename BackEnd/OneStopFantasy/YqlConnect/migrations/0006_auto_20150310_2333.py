# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YqlConnect', '0005_auto_20150310_1133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='processedstats',
            name='athlete',
        ),
        migrations.DeleteModel(
            name='ProcessedStats',
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='assists_Std',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='blocks_Std',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='fieldGoalPercentage_Std',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='freeThrowPercentage_Std',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='points_Std',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='rebounds_Std',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='steals_Std',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='threePointsMade_Std',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monthlydata',
            name='turnovers_Std',
            field=models.FloatField(default=0.0),
            preserve_default=True,
        ),
    ]
