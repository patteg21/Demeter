import time

from django.shortcuts import render
from datetime import datetime
from django.contrib import messages

from storage.forms import *
from .forms import *

from .models import *
from container.models import *
from storage.models import *

# Create your views here.

def dashers(request):

    # Grabs all the facilities to check to see Dasher Location
    facilities = Facility #.objects.all()

    dashers = Dasher.objects.all()
    
    if request.method == 'POST':
        form = DasherMoveForm(request.POST)

        if form.is_valid():
            
            # gets the str form of the dasher requet was made to
            dasherID = request.POST.get('dasher')

            # finds ID assocaited with the current Dasher
            dasher = Dasher.objects.get(dasherID=dasherID)

            # gets the cleaned data version of the request
            location = form.cleaned_data['location']


            #finds a facility associated with that location
            try:
                facility = facilities.objects.get(facilityID=location.facilityID)
            except facilities.DoesNotExist:
                facility = None

            #changes the location to the desired facilities location
            dasher.locationX = facility.locationX
            dasher.locationY = facility.locationY
            dasher.location = facility
    
            # saves the location and the state of the dasher
            dasher.save()

    else:
        form = DasherMoveForm

    return render(request, "storage/dashers.html",{
        "dashers":dashers,
        "form":form,
    })