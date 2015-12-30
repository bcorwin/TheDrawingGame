# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import game.models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_round_game_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rando',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('email_address', models.EmailField(max_length=254)),
                ('confirmation_code', models.CharField(max_length=6, default=game.models.gen_code, unique=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='round',
            name='is_rando',
            field=models.BooleanField(default=False),
        ),
    ]
