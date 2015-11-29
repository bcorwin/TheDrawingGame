# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_length', models.PositiveSmallIntegerField(default=6, validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(15)])),
                ('email_address', models.EmailField(max_length=254)),
                ('game_code', models.CharField(default=b'AjDBBi', unique=True, max_length=6)),
                ('completed', models.BooleanField(default=False)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round_number', models.PositiveSmallIntegerField()),
                ('round_code', models.CharField(default=b'qBvfqh', unique=True, max_length=6)),
                ('round_type', models.CharField(max_length=1, choices=[(b'T', b'Text round'), (b'P', b'Picture round')])),
                ('email_address', models.EmailField(max_length=254)),
                ('submission', models.TextField()),
                ('display_name', models.CharField(max_length=32)),
                ('update_status', models.SmallIntegerField(default=0, choices=[(-1, b'Reset'), (0, b'None'), (1, b'Reminder sent'), (2, b'Request sent'), (3, b'Expired')])),
                ('update_status_date', models.DateTimeField(default=datetime.datetime(2015, 11, 29, 16, 30, 33, 773000, tzinfo=utc))),
                ('completed', models.BooleanField(default=False)),
                ('inserted_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(to='game.Game', on_delete=django.db.models.deletion.PROTECT)),
            ],
        ),
    ]
