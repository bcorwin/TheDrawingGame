from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf

from game.forms import SaveImgForm, make_game, make_new_round, make_picture_round,make_text_round
from game.do import get_round, get_game, select_forms, gen_round_response
    
def show_round(request, code):
    round = None
    type = None
    last_round = False
    
    if request.method == 'POST':
        return HttpResponse(gen_round_response(request.POST))
    else:
        if code not in ['', None]:
            round = get_round(code)
            type = "P" if round.round_type == "T" else "T"
            #to do: if round is complete, say something
            if round.round_number == round.game.game_length - 1: last_round = True
            elif round.game.completed == True:
                pass
                #to do: go to game page
        else: type = "F"
        
        forms = select_forms(type, last_round)
        out = {'round': round, 'type': type, 'last_round': last_round}
        out.update(forms)
        out.update(csrf(request))
        
        return render(request, 'round.html', out)