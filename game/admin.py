from django.contrib import admin
from game.models import Game, Round

class roundInline(admin.TabularInline):
    model = Round
    fields = ['round_number', 'view_round', 'email_address', 'display_name', 'view_submission', 'update_status', 'completed']
    readonly_fields = fields
    show_change_link = False
    extra = 0

class gameAdmin(admin.ModelAdmin):
    list_display = ['game_code', 'email_address', 'game_length', 'completed']
    list_filter = ['email_address', 'game_length', 'completed']
    inlines = [roundInline]
    
class roundAdmin(admin.ModelAdmin):
    list_display = ['round_code', 'round_number', 'display_name', 'email_address', 'update_status', 'update_status_date', 'completed']
    list_filter = ['display_name', 'round_number', 'email_address', 'update_status', 'update_status_date', 'completed']
    fields = ['game', 'round_number', 'view_round', 'round_type', 'display_name', 'email_address', 'update_status', 'update_status_date', 'completed', 'view_submission']
    readonly_fields = ['view_round', 'view_submission']
    
admin.site.register(Game, gameAdmin)
admin.site.register(Round, roundAdmin)