from game.models import Round, Game

def get_round(round):
    r = Round.objects.filter(round_code=round)
    print([t.round_code for t in r])
    out = r.get() if r.exists() else None
    return(out)
    
def get_game(game):
    g = Game.objects.filter(pk=game)
    out = g.get() if g.exists() else None
    return(out)