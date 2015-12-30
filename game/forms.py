from django import forms
from game.models import Round, Game, Rando

class SaveImgForm(forms.Form):
    img = forms.CharField(label='Image', max_length=10000000, widget=forms.HiddenInput(),
            error_messages = {'required': 'Please draw something before submitting.'})
            
class make_game(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["game_length", "email_address"]
        labels = {
            'game_length': ('Number of rounds'),
            'email_address': ('Email address'),
        }
        help_texts = {
            'game_length': ('How many players/rounds.'),
            'email_address': ('Your email address'),
        }
        
class make_new_round(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["display_name", "submission", "email_address"]
        labels = {
            'display_name': ('Name'),
            'submission': ('Sentence'),
            'email_address': ('Next player'),
        }
        help_texts = {
            'display_name': ('Your name'),
            'submission': ('First sentence for the game'),
            'email_address': ('Next player\'s email address'),
        }
        
class make_picture_round(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["display_name", "email_address"]
        labels = {
            'display_name': ('Name'),
            'email_address': ('Next player'),
        }
        help_texts = {
            'display_name': ('Your name'),
            'email_address': ('Next player\'s email address'),
        }
        
class make_text_round(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["submission", "display_name", "email_address"]
        labels = {
            'display_name': ('Name'),
            'submission': ('Your sentence'),
            'email_address': ('Next Player'),
        }
        help_texts = {
            'display_name': ('Your name'),
            'submission': ('Sentence describing the above picture'),
            'email_address': ('Next player\'s email address'),
        }
        
        
class make_last_text(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["submission", "display_name"]
        labels = {
            'display_name': ('Name'),
            'submission': ('Your sentence'),
        }
        help_texts = {
            'display_name': ('Your name'),
            'submission': ('Sentence describing the above picture'),
        }
        
class make_last_picture(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["display_name"]
        labels = {
            'display_name': ('Name'),
        }
        help_texts = {
            'display_name': ('Your name'),
        }
        
class reset_round_form(forms.Form):
    new_email = forms.EmailField()
    
class modify_rando_form(forms.ModelForm):
    class Meta:
        model = Rando
        fields = ["email_address"]
        labels = {
            'email_address': ('Email address'),
        }
        help_texts = {
            'email_address': ('Email address you\'d like to add or remove from the Rando list'),
        }