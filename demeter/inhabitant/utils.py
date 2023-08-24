import time
import random

from .models import *
from container.models import *
from storage.models import *

""""
DEMETER ORIENTED FUNCTIONS
"""
class DemeterEvents():
    # Demeter error messages
    def errorMessage():
        error = [
            "Sorry, can you please rephrase that.",
            "Sorry, can you plese ask a different request.",
            "I cannot understand that request.",
        ]
        return random.choice(error)
        
    def orderDemeter(entities):

        #Looks to see what meal this is 
        if len(entities) >= 2:
            mealType = entities[1]['text'].title()

            mealOptions = TypeRation.objects.filter(mealType=mealType)

            orderOutput = "Here are some options for breakfast foods."
            #returns that back
            return mealType, orderOutput


    def getStatusDemeter(entities):

        #this defines it as a where is Dasher function
        if len(entities) == 2:
            entityName = entities[1]['text']
            if "Dasher" in entityName:
                # grabs the number associated with that dasher
                _ , dasherNumber = entityName.split(" ")

                dasher = Dasher.objects.get(dasherID=dasherNumber)

                return f"{dasher} is at {dasher.location}"

        

    def invokeDemeter(entities):
        for entity in entities:
            print(entity)

class FoodOrder():

    def orderFood(inhabitantID,rationID,facilityID):
        inhabitant = Inhabitant.objects.get(inhabitantID=inhabitantID)
        ration = TypeRation.objects.get(rationID=rationID)
        destinationFacility = Facility.objects.get(facilityID=facilityID)

        #checks to see whether there are any RationPacks to get and if its not 
        querySet = RationPack.objects.filter(typeRation=ration)

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


                nc = NutrientContent.objects.get(ration=ration)
                
                dailyNutrition = DailyNutrition.objects.get(inhabitant=inhabitant)

                # updates all the values of the nutrtion
                dailyNutrition.caloriesConsumed += nc.calories
                dailyNutrition.fatConsumed += nc.fat
                dailyNutrition.proteinConsumed += nc.protein
                dailyNutrition.sodiumConsumed += nc.sodium
                dailyNutrition.fiberConsumed += nc.fiber
                # saves those values
                dailyNutrition.save()