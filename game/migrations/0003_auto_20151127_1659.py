# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_image_test_inserted_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('game_length', models.PositiveSmallIntegerField(default=6, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(15)])),
                ('email_address', models.EmailField(max_length=254)),
                ('game_code', models.CharField(default='YYmjNZ', max_length=6)),
                ('completed', models.BooleanField(default=False)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='pictureRound',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('image', models.TextField()),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('round_number', models.PositiveSmallIntegerField()),
                ('round_code', models.CharField(default='qkZIMc', max_length=6)),
                ('round_type', models.CharField(choices=[('T', 'Text round'), ('P', 'Picture round')], max_length=1)),
                ('email_address', models.EmailField(max_length=254)),
                ('display_name', models.CharField(max_length=32)),
                ('completed', models.NullBooleanField(default=None)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.Game')),
            ],
        ),
        migrations.CreateModel(
            name='textRound',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('sentence', models.CharField(max_length=256)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.Round')),
            ],
        ),
        migrations.AddField(
            model_name='pictureround',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='game.Round'),
        ),
    ]
