from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from random import choice
from string import ascii_letters

class Image_test(models.Model):
    image = models.CharField('Image',max_length=10000000)
    inserted_date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return str(self.id)

def gen_code(n=6):
        return(''.join([choice(ascii_letters) for l in range(n)]))
        
class Game(models.Model):
    game_length = models.PositiveSmallIntegerField(validators=[MinValueValidator(3), MaxValueValidator(15)], default=6)
    email_address = models.EmailField()
    game_code = models.CharField(max_length=6, default=gen_code(n=6))
    completed = models.BooleanField(default=False)
    
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
class Round(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    
    round_number = models.PositiveSmallIntegerField()
    round_code = models.CharField(max_length=6, default=gen_code(n=6))
    round_type = models.CharField(max_length=1, choices=(("T", "Text round"), ("P", "Picture round")))
    
    email_address = models.EmailField()
    submission = models.TextField(blank=True, null=True, default=None)
    display_name = models.CharField(max_length=32)
    
    completed = models.NullBooleanField(default=None)
    
    inserted_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)