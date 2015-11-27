# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20151127_1659'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pictureround',
            name='round',
        ),
        migrations.RemoveField(
            model_name='textround',
            name='round',
        ),
        migrations.AddField(
            model_name='round',
            name='submission',
            field=models.TextField(null=True, default=True, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='game_code',
            field=models.CharField(default='dIGqFP', max_length=6),
        ),
        migrations.AlterField(
            model_name='round',
            name='round_code',
            field=models.CharField(default='ejKHpw', max_length=6),
        ),
        migrations.DeleteModel(
            name='pictureRound',
        ),
        migrations.DeleteModel(
            name='textRound',
        ),
    ]
