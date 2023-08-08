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

#Creates an Empty Container
class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = [
        ]

# orders food for a person
class OrderFoodForm(forms.ModelForm):
    class Meta:
        model = NutrientContent

        fields = [
            "ration",
            # "calories",
            # "fat",
            # "sodium",
            # "fiber",
            # "protein",
        ]
