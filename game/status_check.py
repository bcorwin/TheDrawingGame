from game.models import Round
from django.utils import timezone

def status_check():
    rounds = Round.objects.filter(completed=False, update_status__gte=0)
    
    for r in rounds:
        hours_ago = (timezone.now() - r.update_status_change).total_seconds()/3600

        if r.update_status == 0 and hours_ago >= 24:
            #Send reminder and set status to 1 (reminder sent)
            r.send_reminder_email()
        elif r.update_status == 1 and hours_ago >= 24:
            #Send request and set status to 24
            r.send_request()
        elif r.update_status == 2 and hours_ago >= 24:
            #Set status to -2 (expired) and send final game out
            r.completed = True
            r.set_status(-2)
            
            r.game.completed = True
            r.game.save()
            r.game.send_round_over_email()