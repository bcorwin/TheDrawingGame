from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from random import choice
from string import ascii_letters

def gen_code(n=6):
        return(''.join([choice(ascii_letters) for l in range(n)]))
        
class Game(models.Model):
    game_length = models.PositiveSmallIntegerField(validators=[MinValueValidator(3), MaxValueValidator(15)], default=6)
    email_address = models.EmailField()
    
    game_code = models.CharField(max_length=6, default=gen_code(n=6))
    completed = models.BooleanField(default=False)
    
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def new_code(self):
        out = self.game_code
        chk = out in [g.game_code for g in Game.objects.all()]
        while(chk == True):
            out = gen_code()
            chk = out in [g.game_code for g in Game.objects.all()]
        return(out)
        
    def save(self, *args, **kwargs):
        if not self.pk:
            self.round_code = self.new_code()
        super(Round, self).save(*args, **kwargs)
    
    def __str__(self):
        return(self.game_code)
    
class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    
    round_number = models.PositiveSmallIntegerField()
    round_code = models.CharField(max_length=6, default=gen_code(n=6), unique=True)
    round_type = models.CharField(max_length=1, choices=(("T", "Text round"), ("P", "Picture round")))
    
    email_address = models.EmailField()
    submission = models.TextField()
    display_name = models.CharField(max_length=32)
    
    completed = models.BooleanField(default=False)
    
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def new_code(self):
        out = self.round_code
        chk = out in [r.round_code for r in Round.objects.all()]
        while(chk == True):
            out = gen_code()
            chk = out in [r.round_code for r in Round.objects.all()]
        return(out)
    
    def save(self, *args, **kwargs):
        if not self.pk:
            g = Round.objects.filter(game=self.game).order_by('-round_number')
            self.round_number = g[0].round_number + 1 if g.exists() else 1
            self.round_type = "T" if self.round_number % 2 == 1 else "P"
            self.round_code = self.new_code()
        super(Round, self).save(*args, **kwargs)
    
    def __str__(self):
        return(self.round_code)