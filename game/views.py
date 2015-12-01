from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf

from game.do import get_round, get_game, select_forms, gen_round_response, get_rounds
from game.forms import reset_round_form
    
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
    if request.method == 'POST': code = request.POST["game_code"]
    game = get_game(code)
    if game is not None:
        if game.completed == True:
            rounds = get_rounds(game)
            return render(request, 'view.html', {"rounds":rounds})
        else: return(HttpResponse("This game is not over yet."))
    else:
        return(HttpResponse("This game does not exist"))
        
def wait_round(request, code):
    r = get_round(code)
    if r is not None:
        if r.completed == True:
            return(HttpResponse("This round has been completed."))
        elif r.update_status == 2:
            r.wait_longer()
            return(HttpResponse("Another reminder email has been sent to " + r.email_address + " and given 24 more hours to complete the round."))
        else: return(HttpResponse("Unable to complete wait request."))
    else:
        return(HttpResponse("This round does not exist"))
        
def reset_round(request, code):
    if request.method == "POST":
        form = reset_round_form(request.POST)
        if form.is_valid():
            r = get_round(request.POST["round"])
            new_email = form.cleaned_data["new_email"]
            r.reset_round(new_email)
            return(HttpResponse("Round has been reset! A request to play has been sent to " + new_email + "."))
        else: return(HttpResponse("Email was invalid, try again."))
        
    else:
        r = get_round(code)
        if r is not None:
            if r.completed == True:
                return(HttpResponse("This round has been completed."))
            elif r.update_status == 2:
                form = reset_round_form()
                return(render(request, 'reset.html', {"form":form, "round":r.round_code}))
            else: return(HttpResponse("Unable to complete reset request."))
        else:
            return(HttpResponse("This round does not exist"))

def home(request):
    out = csrf(request)
    return(render_to_response('home.html', out))