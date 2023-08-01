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


def interface(request):
    if request.method == 'POST':
        form = InhabitantForm(request.POST)
        if form.is_valid():
            inhabModel = form.save()
            
            #Automatically creates the associated daily nutrition for a person
            dn = DailyNutrition.objects.create(
                inhabitant=inhabModel,
            )

            messages.success(request, )
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

    return render(request, "inhabitant/movement.html",{
        "numcon":con.objects.count(),
        "rpcon":rp.objects.count(),
        "trcon": tr.objects.count(),
    })



def healthMonitor(request):
    nutrition = DailyNutrition.objects.all()
    inhabitants = Inhabitant.objects.all()
    typeration = TypeRation.objects.all()

    context ={
        "inhabitant": inhabitants,
        "nutrition": nutrition,
        "typeration": typeration,
    }

    return render(request, "inhabitant/health.html",context)


# def inhabDash(request):
#     inhabitants = Inhabitant.objects.all()
#     return render(request, "inhabitant/habDash.html",{
#         'inhabitant': inhabitants,
#     })

def joinInhabDash(request, id):
    inhabitant = Inhabitant.objects.get(inhabitantID='id')
    return render (request, "inhabitant/habDash.html", {
        "inhabitant":inhabitant,
        })






### May Save, keep for now


def orderItems(request):
    inhabitant = Inhabitant
    tr = TypeRation 
    nc = NutrientContent

    initial_data = {
        'caloriesConsumed': DailyNutrition.caloriesConsumed,
        'fatConsumed': DailyNutrition.fatConsumed,
        "sodiumConsumed":DailyNutrition.sodiumConsumed,
        "fiberConsumed": DailyNutrition.fiberConsumed,
        "proteinConsumed": DailyNutrition.proteinConsumed,
    }

    ### Redirect the food iteem data and add it to a person's daily value
    if request.method == 'POST':
        form = OrderFoodForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = OrderFoodForm()

    return render(request, "inhabitant/order.html",{
        "tr": tr.objects.all(),
        "nc": nc.objects.all(),
        "inhabitant":inhabitant.objects.all(),
        "form":form,
    })