# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import game.models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('game_length', models.PositiveSmallIntegerField(default=6, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(15)])),
                ('email_address', models.EmailField(max_length=254)),
                ('game_code', models.CharField(max_length=6, default=game.models.gen_code, unique=True)),
                ('completed', models.BooleanField(default=False)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('round_number', models.PositiveSmallIntegerField()),
                ('round_code', models.CharField(max_length=6, default=game.models.gen_code, unique=True)),
                ('round_type', models.CharField(max_length=1, choices=[('T', 'Text round'), ('P', 'Picture round')])),
                ('email_address', models.EmailField(max_length=254)),
                ('submission', models.TextField()),
                ('display_name', models.CharField(max_length=32)),
                ('update_status', models.SmallIntegerField(default=0, choices=[(-2, 'Expired'), (-1, 'Reset'), (0, 'None'), (1, 'Reminder sent'), (2, 'Request sent')])),
                ('update_status_date', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.Game')),
            ],
        ),
    ]
