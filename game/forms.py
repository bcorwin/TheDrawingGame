from django import forms
from game.models import Round, Game

class SaveImgForm(forms.Form):
    img = forms.CharField(label='Image', max_length=10000000, widget=forms.HiddenInput(),
            error_messages = {'required': 'Please draw something before submitting.'})
            
class make_game(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["game_length", "email_address"]
        
class make_new_round(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["display_name", "submission", "email_address"]
        
class make_picture_round(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["display_name", "email_address"]
        
class make_text_round(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["submission", "display_name", "email_address"]
        
class make_last_text(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["submission", "display_name"]
        
class make_last_picture(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["display_name"]
        
class reset_round_form(forms.Form):
    new_email = forms.EmailField()