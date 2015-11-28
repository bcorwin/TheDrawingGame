from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf

from game.forms import SaveImgForm, make_game, make_new_round, make_picture_round,make_text_round
from game.do import get_round, get_game
    
def show_round(request, code):
    form1 = None
    form2 = None
    form3 = None
    type = None
    round = None
    if request.method == 'POST':
        type = request.POST['type']
        if type == "F":
            form1 = make_game(request.POST, prefix="form1")
            form2 = make_new_round(request.POST, prefix="form2")
            if form1.is_valid() and form2.is_valid():
                g = form1.save()
                r = form2.save(commit=False)
                r.game = g
                r.save()
                return HttpResponse("Thanks for playing!")
        elif type == "P":
            form2 = make_picture_round(request.POST, prefix="form2")
            form3 = SaveImgForm(request.POST)
            if form2.is_valid() and form3.is_valid():
                r = form2.save(commit=False)
                r.game = get_game(request.POST['game'])
                r.round_type = "P"
                r.submission = form3.cleaned_data["img"].replace("data:image/png;base64,", "")
                r.save()
                return HttpResponse("Thanks for playing!")
        elif type == "T":
            form2 = make_picture_round(request.POST, prefix="form2")
            if form2.is_valid():
                r = form2.save(commit=False)
                r.game = get_game(request.POST['game'])
                r.round_type = "T"
                r.save()
                return HttpResponse("Thanks for playing!")

        return HttpResponse(str(form2.errors))
    else:
        if code in ['', None]:
            form1 = make_game(prefix="form1")
            form2 = make_new_round(prefix="form2")
            form3 = None
            round = None
            type = "F"
        else:
            round = get_round(code)
            form1 = None
            if round.round_type == "P":
                type = "T"
                form2 = make_text_round(prefix="form2")
            else:
                type = "P"
                form2 = make_picture_round(prefix="form2")
            form3 = SaveImgForm()
            #get the round type and make proper form
            
    out = {'form1': form1, 'form2': form2, 'form3': form3, 'type': type, 'round': round}
    out.update(csrf(request))
    return render(request, 'round.html', out)