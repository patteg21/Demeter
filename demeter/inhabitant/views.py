#imports for Azure AI
import os
import requests
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

import time
import random

from django.shortcuts import render
from datetime import datetime
from django.contrib import messages
from django.conf import settings

from storage.forms import *
from .forms import *

from .models import *
from container.models import *
from storage.models import *

# functions that are used in demeter
from .utils import DemeterEvents as demEvents




# Create your views here.

def home(request):
    defaultOutput = "Please enter a Question"

    # get the query from the user
    if request.method == 'POST':

        #checks to see what form is getting submitted
        form_name = request.POST.get('demeter-order-food')
        print(form_name)

        if form_name == "demeter-order-food":
            inhabChoice = request.POST.get('inhabOptions')
            mealChoice = request.POST.get('mealOptions')
            facilityChoice = request.POST.get('facilityOptions')


            demeterCompleteOrder = f"Thanks {inhabChoice}! I will delivery your meal to {facilityChoice}"
            
            return render(request,"inhabitant/home.html",{
            "demeterOutput":demeterCompleteOrder
        
            })

            


    
        #gets the question that is being asked
        queryInput = request.POST.get('queryInput')
        
        #collects the keys that are going to be used
        clu_endpoint = os.environ["AZURE_CONVERSATIONS_ENDPOINT"]
        clu_key = os.environ["AZURE_CONVERSATIONS_KEY"]
        project_name = os.environ["AZURE_CONVERSATIONS_PROJECT_NAME"]
        deployment_name = os.environ["AZURE_CONVERSATIONS_DEPLOYMENT_NAME"]
        
        # analyze query
        client = ConversationAnalysisClient(clu_endpoint, AzureKeyCredential(clu_key))
        with client:
            query = queryInput
            result = client.analyze_conversation(
                task={
                    "kind": "Conversation",
                    "analysisInput": {
                        "conversationItem": {
                            "participantId": "1",
                            "id": "1",
                            "modality": "text",
                            "language": "en",
                            "text": query
                        },
                        "isLoggingEnabled": False
                    },
                    "parameters": {
                        "projectName": project_name,
                        "deploymentName": deployment_name,
                        "verbose": True
                    }
                }
            )

        # print(f"query: {result['result']['query']}")
        # print(f"project kind: {result['result']['prediction']['projectKind']}\n")

        # print(f"top intent: {result['result']['prediction']['topIntent']}")
        # print(f"category: {result['result']['prediction']['intents'][0]['category']}")
        # print(f"confidence score: {result['result']['prediction']['intents'][0]['confidenceScore']}\n")

        # print("entities:")
        # for entity in result['result']['prediction']['entities']:
        #     print(f"\ncategory: {entity['category']}")
        #     print(f"text: {entity['text']}")
        #     print(f"confidence score: {entity['confidenceScore']}")
        #     if "resolutions" in entity:
        #         print("resolutions")
        #         for resolution in entity['resolutions']:
        #             print(f"kind: {resolution['resolutionKind']}")
        #             print(f"value: {resolution['value']}")
        #     if "extraInformation" in entity:
        #         print("extra info")
        #         for data in entity['extraInformation']:
        #             print(f"kind: {data['extraInformationKind']}")
        #             if data['extraInformationKind'] == "ListKey":
        #                 print(f"key: {data['key']}")
        #             if data['extraInformationKind'] == "EntitySubtype":
        #                 print(f"value: {data['value']}")

        # if there is low confidence in message, throws an error output
        confidenceScore = result['result']['prediction']['intents'][0]['confidenceScore']
        if confidenceScore < 0.70:
            return render(request,"inhabitant/home.html",{
            "demeterOutput":demEvents.errorMessage,
        })

        #topIntent of request, lowercases the resulting string
        topIntent = (result['result']['prediction']['topIntent']).lower()

        #defines variables that need to passed to functions
        entities = result['result']['prediction']['entities']
        
        # call the correct function based on intent
        if topIntent == "order":
            mealType, orderOutput = demEvents.orderDemeter(entities)

            facilityOptions = Facility.objects.filter(typeFacility="Living")
            mealOptions = TypeRation.objects.filter(mealType=mealType)
            inhabitantOptions = Inhabitant.objects.all()

            orderForm = True
            
            return render(request,"inhabitant/home.html",{
                "demeterOutput":orderOutput,
                "inhabitantOptions":inhabitantOptions,
                "mealOptions":mealOptions,
                "facilityOptions":facilityOptions,
                "orderForm":orderForm,
            })
        
        elif topIntent == "getstatus":
            getStatusOutput = demEvents.getStatusDemeter(entities)
            return render(request,"inhabitant/home.html",{
                "demeterOutput":getStatusOutput,
            })
        elif topIntent == "invoke":
            demEvents.invokeDemeter(entities)




    return render(request,"inhabitant/home.html",{
        "demeterOutput":defaultOutput,
        
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
                    optimalDasher = availableDashers[0]
                    
                    ###-------------------ALGORITHM-------------------------###

                    # if len(availableDashers) > 1:
                    #     optimalManhattan = (abs(potentialDasher.locationX-locationOfRation.locationX)+ abs(potentialDasher.locationY-locationOfRation.locationY)) + (abs(potentialDasher.locationX - destinationFacility.locationX) + abs(potentialDasher.locationY - destinationFacility.locationX))
                    #     for potentialDasher in availableDashers[1:]:

                    #         # the manhattan distacne to the ration facility or Destination
                    #         distanceFacility = (abs(potentialDasher.locationX-locationOfRation.locationX)+ abs(potentialDasher.locationY-locationOfRation.locationY))
                    #         distanceDestination = (abs(potentialDasher.locationX - destinationFacility.locationX) + abs(potentialDasher.locationY - destinationFacility.locationX))

                    #         potentialManhattan = distanceFacility + distanceDestination

                    #         if potentialManhattan < optimalManhattan:
                    #             optimalManhattan = potentialManhattan
                    #             optimalDasher = potentialDasher
                                
                    
                    ##-----------------------------------------------###

                    # changes the status so that it is no longer Awaiting
                    optimalDasher.status = "In-Progress"

                    #moves the dasher to the location of the ration
                    optimalDasher.location = locationOfRation
                    optimalDasher.locationX = locationOfRation.locationX
                    optimalDasher.locationY = locationOfRation.locationY
                    
                    #saves the change to the location
                    optimalDasher.save()

                    # Grabs ration and removes it from the rationPack
                    optimalDasher.rationHeld = ration
                    rationPack.rations -= 1
                    rationPack.save()
                    optimalDasher.save()
                    
                    #movement time simulation   ------> Change!!!!!!

                    # changes the location
                    optimalDasher.location = destinationFacility
                    optimalDasher.locationX = destinationFacility.locationX
                    optimalDasher.locationY = destinationFacility.locationY
                    
                    # saves the location change
                    optimalDasher.save()
                    
                    # removes the ration and saves the changes
                    optimalDasher.rationHeld = None
                    optimalDasher.status = "Awaiting"
                    optimalDasher.save()



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