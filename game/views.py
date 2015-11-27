from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect

from .forms import SaveImgForm, firstRound

from game.models import Image_test

# Create your views here.
def canvas(request):
    img = None
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SaveImgForm(request.POST)
        # check whether it's valid:
        
        if form.is_valid():
            img = form.cleaned_data["img"].replace("data:image/png;base64,", "")
            
            i = Image_test(image = img)
            i.save()
            
            return HttpResponseRedirect('')
    # if a GET (or any other method) we'll create a blank form
    else: form = SaveImgForm()
    
    return render(request, 'canvas.html', {'form': form})
    
def image(request, ImageID):
    image = Image_test.objects.get(pk=ImageID).image
    data = {'image': image}
    
    return render(request, 'image.html', data)
    
def show_round(request, code):
    if code in ['', None]:
        form = firstRound(initial={'round_type': "T"})
    else:
        pass
        #get the round type and make proper form
    
    return render(request, 'round.html', {'form': form})