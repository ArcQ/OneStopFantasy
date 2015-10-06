# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YqlConnect', '0006_auto_20150310_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailydata',
            name='athlete',
        ),
        migrations.DeleteModel(
            name='DailyData',
        ),
        migrations.RemoveField(
            model_name='lasttengameaverages',
            name='athlete',
        ),
        migrations.DeleteModel(
            name='LastTenGameAverages',
        ),
        migrations.RemoveField(
            model_name='lasttwentygameaverages',
            name='athlete',
        ),
        migrations.DeleteModel(
            name='LastTwentyGameAverages',
        ),
        migrations.RemoveField(
            model_name='monthlydata',
            name='athlete',
        ),
        migrations.DeleteModel(
            name='MonthlyData',
        ),
    ]
