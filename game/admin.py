from django.contrib import admin
from game.models import Game, Round

class roundInline(admin.TabularInline):
    model = Round
    fields = ['round_number', 'round_code', 'round_type', 'email_address', 'display_name', 'completed']
    readonly_fields = fields
    show_change_link = True
    extra = 0

class gameAdmin(admin.ModelAdmin):
    list_display = ['game_code', 'email_address', 'game_length', 'completed']
    list_filter = ['email_address', 'game_length', 'completed']
    inlines = [roundInline]
    
admin.site.register(Game, gameAdmin)
admin.site.register(Round)
#Show images in admin not base 64