from django.contrib import admin, messages
from game.models import Game, Round

def send_request(modeladmin, request, queryset):
    if len(queryset) == 0: messages.error(request, "No rounds selected.")
    for round in queryset:
        if (round.update_status >= 1 and round.completed == False):
            round.send_request()
            messages.info(request, "Request sent for round " + round.round_code)
        else: messages.warning(request, "Request not sent for round " + round.round_code )
    

def send_reminder(modeladmin, request, queryset):
    if len(queryset) == 0: messages.error(request, "No rounds selected.")
    for round in queryset:
        if (round.update_status >= 0 and round.completed == False):
            round.send_reminder_email()
            messages.info(request, "Email sent to " + round.email_address)
        else: messages.warning(request, "Email not sent to " + round.email_address)

class roundInline(admin.TabularInline):
    model = Round
    fields = ['round_number', 'view_round', 'display_name', 'email_address', 'view_submission', 'update_status', 'completed']
    readonly_fields = fields
    show_change_link = True
    extra = 0

class gameAdmin(admin.ModelAdmin):
    list_display = ['game_code', 'email_address', 'game_length', 'completed']
    list_filter = ['email_address', 'game_length', 'completed']
    fields = ['view_game', 'game_length', 'email_address', 'completed']
    readonly_fields = ['view_game']
    inlines = [roundInline]
    
class roundAdmin(admin.ModelAdmin):
    list_display = ['round_code', 'round_number', 'display_name', 'email_address', 'update_status', 'update_status_date', 'completed', 'game_number']
    search_fields = ['round_code', 'display_name', 'email_address']
    ordering = ['-game_number', '-round_number']
    list_filter = ['update_status', 'update_status_date', 'completed']
    fields = ['game', 'round_number', 'view_round', 'round_type', 'display_name', 'email_address', 'update_status', 'update_status_date', 'completed', 'view_submission']
    readonly_fields = ['view_round', 'view_submission', 'update_status_date']
    actions = [send_reminder, send_request]
    
admin.site.register(Game, gameAdmin)
admin.site.register(Round, roundAdmin)