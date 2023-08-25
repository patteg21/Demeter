from django import forms
from container.models import *
from .models import *
from inhabitant.models import *

# Define forms below

class DasherMoveForm(forms.ModelForm):
    class Meta:
        model = Dasher
        # fields = "__all__"
        fields = [
            "location"
            ] 
            
        # the way the input will be labeled
        labels = {
            "location":""
        }


        widgets = {
            'location': forms.Select(attrs={'class': 'model-form'})
        }


# allows you to choose a specifc facility    
class FacilityForm(forms.Form):
    facility = forms.ModelChoiceField(queryset=Facility.objects.all())