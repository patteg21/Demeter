from django import forms
from .models import *
from container.models import * 

class InhabitantForm(forms.ModelForm):
    class Meta:
        model = Inhabitant
        # fields = "__all__"
        fields = [
            "firstName",
            "lastName",
            "inhabitantID",
            "height",
            "weight",
            "status",
            ]

class OrderFoodForm(forms.ModelForm):
    class Meta:
        model = DailyNutrition
        fields =[
        "dailyNutrition",
        "inhabitant",
        "dateStamp",
        "caloriesConsumed", 
        "fatConsumed",
        "sodiumConsumed", 
        "fiberConsumed",
        "proteinConsumed",
        ]