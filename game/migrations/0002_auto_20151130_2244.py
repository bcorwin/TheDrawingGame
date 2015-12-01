# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_code',
            field=models.CharField(default=b'zsrAmT', unique=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='round',
            name='round_code',
            field=models.CharField(default=b'qIoWaE', unique=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='round',
            name='update_status',
            field=models.SmallIntegerField(default=0, choices=[(-2, b'Expired'), (-1, b'Reset'), (0, b'None'), (1, b'Reminder sent'), (2, b'Request sent')]),
        ),
        migrations.AlterField(
            model_name='round',
            name='update_status_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 12, 1, 4, 44, 12, 354000, tzinfo=utc)),
        ),
    ]
