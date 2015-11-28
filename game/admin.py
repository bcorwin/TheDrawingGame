from django.contrib import admin
from game.models import Game, Round

admin.site.register(Game)
admin.site.register(Round)
#Show images in admin not base 64