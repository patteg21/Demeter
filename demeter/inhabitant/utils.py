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