from django.shortcuts import render
from datetime import datetime
from django.contrib import messages

from storage.forms import *
from .forms import *

from .models import *
from container.models import *
from storage.models import *



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

    dashers = Dasher.objects.all()
    


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
            facility = facilityForm.cleaned_data['facility']
            
            
            # cleans the raion input
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
                

                if rationPack.rations > 0:
                    # removes a ration from the RationPack
                    rationPack.rations -= 1

                    rationPack.save()
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