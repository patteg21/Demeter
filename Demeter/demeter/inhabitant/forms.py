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

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = [
        ]