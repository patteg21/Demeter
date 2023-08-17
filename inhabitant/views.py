import time

from django.shortcuts import render
from datetime import datetime
from django.contrib import messages

from storage.forms import *
from .forms import *

from .models import *
from container.models import *
from storage.models import *

#test
# Create your views here.
def home(request):
    return render(request,"inhabitant/base.html",{
        "test":"Test worked"
    })

###
def interface(request):
    
    return render(request, "inhabitant/interface.html",{
        })

def containers(request):
    con = Container
    tr = TypeRation
    rp = RationPack
    nc = NutrientContent

    # form for adding another container 
    if request.method == 'POST':
        form = ContainerForm(request.POST)
        if form.is_valid():


            # will not save a container if there are 25 of more containers
            if con.objects.count() >= 100:
                pass
            else:
                form.save()
    else:
        form = ContainerForm


    return render(request, "inhabitant/containers.html",{
        "form":form,
        "containers": con.objects.all(),
        "numcon":con.objects.count(),
        "rpcon":rp.objects.count(),
        "trcon": tr.objects.count(),
    })



def healthMonitor(request):
    nutrition = DailyNutrition.objects.all()
    inhabitants = Inhabitant.objects.all()
    typeRation = TypeRation.objects.all()

    ## create a 
    if request.method == 'POST':
        form = InhabitantForm(request.POST)
        if form.is_valid():
            inhabModel = form.save()
            
            #Automatically creates the associated daily nutrition for a person
            dn = DailyNutrition.objects.create(
                inhabitant=inhabModel,
            )
    else:
        form = InhabitantForm()

    context ={
        "inhabitant": inhabitants,
        "nutrition": nutrition,
        "form":form,
    }

    return render(request, "inhabitant/monitor.html",context)


# individual persons order space to include intake of food
def joinInhabDash(request, inhabitantID):  
    ### creates a dynamic url based on a an Inhabitant's ID


    #creates a dynamic url based on inhabitants id
    try:
        inhabitant = Inhabitant.objects.get(inhabitantID=inhabitantID)
        dailyNutrition = DailyNutrition.objects.get(inhabitant=inhabitant)
    except Inhabitant.DoesNotExist:
        inhabitant = None


    # creates a form to order food for that particular person
    if request.method == 'POST':
        
        # Passes the Nutrient Content model in a form
        form = OrderFoodForm(request.POST)
        facilityForm = FacilityForm(request.POST)

        # displays the option of choosing rations
        if form.is_valid() and facilityForm.is_valid():

            # grabs the facility the shipment is going to
            destinationFacility = facilityForm.cleaned_data['facility']

            # cleans the ration input
            ration = form.cleaned_data['ration']


            #checks to see whether there are any RationPacks to get and if its not 
            querySet = RationPack.objects.filter(typeRation=ration)

            # checks to see if queryset came out with any results  
            if len(querySet) >= 1:
                
                # this is to rotate through the rationpacks if one is empty
                # without getting rid of empty ones
                for query in querySet:
                    rationPack = query
                    if rationPack.rations > 0:
                        break 
                
                #checks to see if the rationpack is not empty
                if rationPack.rations > 0:

                    #turned into model form (not actually necessary)
                    destinationFacility = Facility.objects.get(facilityID=destinationFacility.facilityID)

                    # prints the location of ration where there is that ration
                    locationOfRation = rationPack.container.location

                    # finds dashers awaiting orders
                    availableDashers = Dasher.objects.filter(status="Awaiting")

                    # grabs the first dasher available (replace with algorithm)
                    dasherFirst = availableDashers[0]
                    
                    ###-----------------------------------------------###
                    #              BEST DASHER ALGORITHM                #
                    

                    # optimalDasher = None
                    # bestManhattan = 
                

                    # for potentialDasher in availableDashers:

                    #     # the manhattan distacne to the ration facility or Destination
                    #     distanceFacility = (abs(potentialDasher.locationX-locationOfRation.locationX)+ abs(potentialDasher.locationY-locationOfRation.locationY))
                    #     distanceDestination = (abs(potentialDasher.locationX - destinationFacility.locationX) + abs(potentialDasher.locationY - destinationFacility.locationX))

                    #     if distanceFacility + distanceDestination 
                    
                    ###-----------------------------------------------###

                    # changes the status so that it is no longer Awaiting
                    dasherFirst.status = "In-Progress"

                    #moves the dasher to the location of the ration
                    dasherFirst.location = locationOfRation
                    dasherFirst.locationX = locationOfRation.locationX
                    dasherFirst.locationY = locationOfRation.locationY
                    
                    #saves the change to the location
                    dasherFirst.save()

                    # Grabs ration and removes it from the rationPack
                    dasherFirst.rationHeld = ration
                    rationPack.rations -= 1
                    rationPack.save()
                    dasherFirst.save()
                    
                    #movement time simulation   ------> Change!!!!!!

                    # changes the location
                    dasherFirst.location = destinationFacility
                    dasherFirst.locationX = destinationFacility.locationX
                    dasherFirst.locationY = destinationFacility.locationY
                    
                    # saves the location change
                    dasherFirst.save()
                    
                    # removes the ration and saves the changes
                    dasherFirst.rationHeld = None
                    dasherFirst.status = "Awaiting"
                    dasherFirst.save()



                else:
                    return render(request,"inhabitant/habdash.html",{
                    "inhabitant":inhabitant,
                    "nutrition":dailyNutrition,
                    "form":form,
                    "rationPack":RationPack,
                    "rationDNE":True,
                    "facilityForm":facilityForm,
                    })
            else:
                return render(request,"inhabitant/habdash.html",{
                    "inhabitant":inhabitant,
                    "nutrition":dailyNutrition,
                    "form":form,
                    "rationPack":RationPack,
                    "rationDNE":True,
                    "facilityForm":facilityForm,
                    })


            #uses the input to get correct associated nutrients
            nc = NutrientContent.objects.get(ration=ration)

            # updates all the values of the nutrtion
            dailyNutrition.caloriesConsumed += nc.calories
            dailyNutrition.fatConsumed += nc.fat
            dailyNutrition.proteinConsumed += nc.protein
            dailyNutrition.sodiumConsumed += nc.sodium
            dailyNutrition.fiberConsumed += nc.fiber
            # saves those values
            dailyNutrition.save()

    else:
        form = OrderFoodForm()
        facilityForm = FacilityForm()

    
    return render(request,"inhabitant/habdash.html",{
        "inhabitant":inhabitant,
        "nutrition":dailyNutrition,
        "form":form,
        "RationDNE":False,
        "rationPack":RationPack,
        "facilityForm":facilityForm,
        })


def facilities(request):

    facilities = Facility.objects.all()

    return render(request, "inhabitant/facilities.html",{
        "facilities":facilities,
    })

def joinFacilityDash(request, facilityID):


    # grabs the unique facility that is associated with a url
    try:
        facility = Facility.objects.get(facilityID=facilityID)
        containers = Container.objects.filter(location=facility)
    except Inhabitant.DoesNotExist:
        facility = None





    return render(request, "inhabitant/facilitydash.html",{
        "facility":facility,
        "containers":containers,

    })