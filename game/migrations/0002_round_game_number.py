# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='game_number',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
