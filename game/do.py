from game.models import Round, Game
import game.forms as forms


def get_round(round):
    r = Round.objects.filter(round_code=round)
    out = r.get() if r.exists() else None
    return(out)
    
def get_game(game):
    g = Game.objects.filter(pk=game)
    out = g.get() if g.exists() else None
    return(out)
    
def select_forms(round_type, last_round=False):
    out = {"form1": None, "form2": None, "form3": None}
    if round_type == "F":
        out["form1"] = forms.make_game(prefix="form1")
        out["form2"] = forms.make_new_round(prefix="form2")
    elif round_type == "T":
        out["form2"] = forms.make_text_round(prefix="form2") if last_round == False else forms.make_last_text(prefix="form2")
    elif round_type == "P":
        out["form3"] = forms.SaveImgForm()
        out["form2"] = forms.make_picture_round(prefix="form2") if last_round == False else forms.make_last_picture(prefix="form2")
    return(out)
    
def gen_round_response(post_data):
    try: last_round = post_data['last_round'] == "True"
    except: last_round = None
    try: round_type = post_data['type']
    except: round_type = None
    
    messages = {"success": "Thanks for playing!", "unknowntype": "Unknown round_type."}
    
    if round_type == "F":
        form1 = forms.make_game(post_data, prefix="form1")
        form2 = forms.make_new_round(post_data, prefix="form2")
        if form1.is_valid() and form2.is_valid():
            g = form1.save()
            
            r = form2.save(commit=False)
            r.round_type = "T"
            r.game = g
            
            r.save()
            out = messages["success"]
        else: out = str(form1.errors) + str(form2.errors)
    elif round_type == "T":
        form2 = forms.make_text_round(post_data, prefix="form2") if last_round == False else forms.make_last_text(post_data, prefix="form2")
        if form2.is_valid():
            r = form2.save(commit=False)
            
            r.game = get_game(post_data['game'])
            r.round_type = "T"
            if last_round == True: r.email_address = r.game.email_address
            
            r.save()
            out = messages["success"]
        else: out = str(form2.errors)   
    elif round_type == "P":
        form2 = forms.make_picture_round(post_data, prefix="form2") if last_round == False else forms.make_last_picture(post_data, prefix="form2")
        form3 = forms.SaveImgForm(post_data)
        if form2.is_valid() and form3.is_valid():
            r = form2.save(commit=False)
            
            r.game = get_game(post_data['game'])
            r.round_type = "P"
            r.submission = form3.cleaned_data["img"].replace("data:image/png;base64,", "")
            if last_round == True: r.email_address = r.game.email_address
            
            r.save()
            out = messages["success"]
        else: out = str(form2.errors)
    else: out = messages["unknowntype"]
    return(out)
    