# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('YqlConnect', '0004_auto_20150310_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='PositionToAthlete',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.CharField(max_length=5, null=True)),
                ('athlete', models.ForeignKey(related_name='PositionToAthlete_Athlete', to='YqlConnect.Athlete', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='athlete',
            name='positions',
            field=models.CharField(default='none', max_length=200),
            preserve_default=False,
        ),
    ]
