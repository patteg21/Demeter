from django.shortcuts import render
from django.contrib import messages
from .forms import *
from .models import *
from container.models import *



# Create your views here.
def home(request):
    return render(request,"inhabitant/base.html",{
        "test":"Test worked"
    })

###
def interface(request):
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
    
    return render(request, "inhabitant/interface.html",{
            "form": form,
        })

def movement(request):
    con = Container
    tr = TypeRation
    rp = RationPack
    nc = NutrientContent

    # form for adding another container 
    if request.method == 'POST':
        form = ContainerForm(request.POST)
        if form.is_valid():

            # will not save a container if there are 25 of more containers
            if con.objects.count() >= 25:
                pass
            else:
                form.save()
    else:
        form = ContainerForm


    return render(request, "inhabitant/movement.html",{
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



def joinInhabDash(request, inhabitantID):  

    ### creates a dynamic url based on a an Inhabitant's ID
    try:
        inhabitant = Inhabitant.objects.get(inhabitantID=inhabitantID)
    except Inhabitant.DoesNotExist:
        inhabitant = None
    
    return render(request,"inhabitant/habdash.html",{
        "inhabitant":inhabitant,
        })




### May Save, keep for now
def orderItems(request):
    inhabitant = Inhabitant
    tr = TypeRation 
    nc = NutrientContent

    ### Redirect the food iteem data and add it to a person's daily value
    return render(request, "inhabitant/order.html",{
        "tr": tr.objects.all(),
        "nc": nc.objects.all(),
        "inhabitant":inhabitant.objects.all(),
    })