from django.contrib import admin
from game.models import Game, Round

class roundInline(admin.TabularInline):
    model = Round
    fields = ['round_number', 'round_code', 'email_address', 'display_name', 'view_submission', 'completed']
    readonly_fields = fields
    show_change_link = True
    extra = 0

class gameAdmin(admin.ModelAdmin):
    list_display = ['game_code', 'email_address', 'game_length', 'completed']
    list_filter = ['email_address', 'game_length', 'completed']
    inlines = [roundInline]
    
class roundAdmin(admin.ModelAdmin):
    list_display = ['round_code', 'round_number', 'display_name', 'email_address', 'completed']
    list_filter = ['display_name', 'round_number', 'email_address', 'completed']
    fields = ['game', 'round_number', 'round_code', 'round_type', 'display_name', 'email_address', 'view_submission']
    readonly_fields = ['view_submission']
    
admin.site.register(Game, gameAdmin)
admin.site.register(Round, roundAdmin)
#Show images in admin not base 64