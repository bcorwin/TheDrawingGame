from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf

from game.do import get_round, get_game, select_forms, gen_round_response, get_rounds
    
def show_round(request, code):
    round = None
    type = None
    last_round = False
    
    if request.method == 'POST':
        return(HttpResponse(gen_round_response(request.POST)))
    else:
        if code not in ['', None]:
            round = get_round(code)
            type = "P" if round.round_type == "T" else "T"
            
            if round.completed == True and round.game.completed == False:
                return(HttpResponse("This round has been completed. However the game is not over yet."))
            elif round.game.completed == True:
                return(HttpResponseRedirect("/game/view/" + round.game.game_code))
            if round.round_number == round.game.game_length - 1:
                last_round = True
        else: type = "F"
        
        forms = select_forms(type, last_round)
        out = {'round': round, 'type': type, 'last_round': last_round}
        out.update(forms)
        out.update(csrf(request))
        
        return(render(request, 'round.html', out))
        
def view_game(request, code):
    game = get_game(code)
    if game is not None:
        if game.completed == True:
            rounds = get_rounds(game)
            return render(request, 'view.html', {"rounds":rounds})
        else: return(HttpResponse("This game is not over yet."))
    else:
        return(HttpResponse("This game does not exist"))
