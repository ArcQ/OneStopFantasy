# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YqlConnect', '0002_monthlydata_processedstats_weeklydata'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextended',
            name='oauth_Token',
            field=models.TextField(max_length=8000, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userextended',
            name='oauth_Token_Secret',
            field=models.TextField(max_length=8000, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userextended',
            name='oauth_Verifier',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userextended',
            name='access_Token',
            field=models.TextField(max_length=8000, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userextended',
            name='access_Token_Secret',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userextended',
            name='oauth_session_handle',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
    ]
