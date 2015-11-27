from django import forms
from game.models import Round

class SaveImgForm(forms.Form):
    img = forms.CharField(label='Image', max_length=10000000, widget=forms.HiddenInput(),
            error_messages = {'required': 'Please draw something before submitting.'})
            
class firstRound(forms.ModelForm):
    class Meta:
        model = Round
        fields = ["display_name", "submission", "email_address", "round_type"]
        widgets = {"round_type": forms.HiddenInput()}