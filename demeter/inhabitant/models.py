from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator
import uuid

# Create your models here.

class Inhabitant(models.Model):
    STATUS = [
    ("Healthy", "Healthy"),
    ("Sick", "Sick"),
    ("Recovering","Recovering"),
    ("Injured","Injured"),
    ("Deceased","Deceased"),
    ]   

    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)

    inhabitantID = models.CharField(max_length=64,primary_key=True)
    height =models.IntegerField(blank=False)
    weight = models.IntegerField(blank=False)

    status = models.CharField(max_length=64,default="Healthy",choices=STATUS)

    #Defaults are set to it so that allergies and intolerances are assumed
    isVegetarian = models.BooleanField(default=False)
    allergyGluten = models.BooleanField(default=False)
    allergyDairy = models.BooleanField(default=False)

    def __str__ (self):
        return f"{self.firstName} {self.lastName}"



class DailyNutrition(models.Model):
    # UUID field for each instance of Daily Nutrition
    dailyNutrition = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    
    # FOREIGN KEYS
    inhabitant = models.ForeignKey(Inhabitant, on_delete=models.CASCADE, related_name="Nutrition")

    # DATE set automatically to each day that calories are registered
    dateStamp = models.DateField(default=datetime.today)
    timeStamp = models.DateTimeField(default=datetime.now)

    # List of food Eaten. Should be [food,timeStamp]
    foodEaten = models.TextField(null=True, blank=True)

    # min value set to 0,
    caloriesConsumed = models.IntegerField(default=0, blank=False, null=False, validators=[MinValueValidator(0)])
    fatConsumed = models.IntegerField(default=0, blank=False, null=False, validators=[MinValueValidator(0)])
    sodiumConsumed = models.IntegerField(default=0, blank=False, null=False, validators=[MinValueValidator(0)])
    fiberConsumed = models.IntegerField(default=0, blank=False, null=False, validators=[MinValueValidator(0)])
    proteinConsumed = models.IntegerField(default=0, blank=False, null=False, validators=[MinValueValidator(0)])


    def __str__ (self):
        return f"{self.inhabitant} Nutrition {self.dateStamp}"
    

